#!/usr/bin/env python3
"""Aplicação Streamlit para geração automática de atas de reunião."""

import os
import tempfile

import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

from ata_reuniao_core import (
    PROMPT_1_PREVIA,
    build_prompt_2_for_word,
    compose_preview_text,
    extract_template_blueprint,
    extrair_nome_arquivo,
    extrair_texto_arquivo,
    fill_template_by_spec,
    parse_preview_text,
    preview_to_payload,
    render_template_overview,
)


load_dotenv()

st.set_page_config(
    page_title="Gerador de Atas de Reunião",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📋 Gerador Automático de Atas de Reunião")
st.caption("Duas chamadas ao modelo: pré-ata em texto puro e plano de gravação no template")


def get_client() -> tuple[AzureOpenAI, str]:
    client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise RuntimeError("AZURE_OPENAI_DEPLOYMENT não está definido no .env")
    return client, deployment


def init_state() -> None:
    st.session_state.setdefault("preview_text", "")
    st.session_state.setdefault("generation_report", None)
    st.session_state.setdefault("template_overview", "")
    st.session_state.setdefault("template_blueprint", None)
    st.session_state.setdefault("transcricao_nome_arquivo", "")


def call_model_text(prompt: str, content: str, max_tokens: int = 4000) -> str:
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "system",
                "content": "Você trabalha com atas de reunião e segue rigorosamente o formato solicitado.",
            },
            {
                "role": "user",
                "content": f"{prompt}\n\nENTRADA:\n{content}",
            },
        ],
        max_completion_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("### Modelo em uso")
        st.write(deployment)
        st.markdown("### Fluxo")
        st.text(
            "1. A transcrição vira uma pré-ata em texto puro.\n"
            "2. Você revisa e edita antes de gerar.\n"
            "3. A gravação no template segue a estrutura fixa validada."
        )


def render_guided_editor() -> None:
    if not st.session_state.get("preview_text"):
        return

    parsed = parse_preview_text(st.session_state["preview_text"])
    with st.expander("Editar antes de gerar", expanded=False):
        with st.form("guided_editor_form"):
            cliente = st.text_input("Cliente", value=parsed["cliente"])
            projeto = st.text_input("Nome e Código do projeto", value=parsed["nome_codigo_projeto"])
            data_reuniao = st.text_input("Data da Reunião", value=parsed["data_reuniao"])
            hora = st.text_input("Horas", value=parsed["horas"])
            data_documento = st.text_input("Data de criação do Documento", value=parsed["data_documento"])
            convocados = st.text_area(
                "Convocados",
                value="\n".join(parsed["convocados"]),
                height=120,
                help="Uma linha por convocado: Nome | Setor | Sim ou Não",
            )
            pauta = st.text_area("Pauta", value="\n".join(parsed["pauta"]), height=120)
            definicoes = st.text_area("Definições", value="\n".join(parsed["definicoes"]), height=120)
            pendencias = st.text_area(
                "Pendências",
                value="\n".join(parsed["pendencias"]),
                height=120,
                help="Uma linha por item: Descrição | Responsável | Prazo",
            )
            plano_acao = st.text_area(
                "Plano de ação",
                value="\n".join(parsed["plano_acao"]),
                height=120,
                help="Uma linha por item: Descrição | Responsável | Prazo",
            )

            submitted = st.form_submit_button("Aplicar alterações ao preview")
            if submitted:
                st.session_state["preview_text"] = compose_preview_text(
                    {
                        "cliente": cliente,
                        "nome_codigo_projeto": projeto,
                        "data_reuniao": data_reuniao,
                        "horas": hora,
                        "data_documento": data_documento,
                        "convocados": [line.strip() for line in convocados.splitlines() if line.strip()],
                        "pauta": [line.strip() for line in pauta.splitlines() if line.strip()],
                        "definicoes": [line.strip() for line in definicoes.splitlines() if line.strip()],
                        "pendencias": [line.strip() for line in pendencias.splitlines() if line.strip()],
                        "plano_acao": [line.strip() for line in plano_acao.splitlines() if line.strip()],
                    }
                )
                st.success("Preview atualizado.")


try:
    client, deployment = get_client()
except Exception as exc:
    st.error(f"Erro na configuração do Azure OpenAI: {exc}")
    st.stop()

init_state()
render_sidebar()

tab1, tab2 = st.tabs(["Processar", "Instruções"])

with tab1:
    left_col, right_col = st.columns(2)

    with left_col:
        transcription_file = st.file_uploader(
            "Transcrição",
            type=["txt", "md", "docx"],
            help="Use um arquivo exportado do Teams, TXT ou Markdown.",
        )
        pasted_text = st.text_area(
            "Ou cole a transcrição",
            height=240,
            placeholder="Cole aqui a transcrição completa da reunião.",
        )

    with right_col:
        template_file = st.file_uploader(
            "Template DOCX",
            type=["docx"],
            help="O template real que será preenchido.",
        )

    transcription_text = pasted_text.strip() if pasted_text.strip() else extrair_texto_arquivo(transcription_file) or ""
    if pasted_text.strip():
        st.session_state["transcricao_nome_arquivo"] = "texto_colado.txt"
    elif transcription_file is not None:
        st.session_state["transcricao_nome_arquivo"] = transcription_file.name

    if transcription_text:
        with st.expander("Prévia da transcrição extraída", expanded=False):
            st.text_area("Transcrição", value=transcription_text[:8000], height=260, disabled=True)

    if template_file is not None:
        blueprint = extract_template_blueprint(template_file.getvalue())
        st.session_state["template_blueprint"] = blueprint
        st.session_state["template_overview"] = render_template_overview(blueprint)
        with st.expander("Leitura do template", expanded=False):
            st.text_area("Template analisado", value=st.session_state["template_overview"], height=320, disabled=True)

    if st.button("1. Gerar prévia da ata", use_container_width=True, type="primary"):
        if not transcription_text:
            st.error("Forneça uma transcrição para análise.")
        else:
            with st.spinner("Gerando prévia da ata..."):
                try:
                    contexto_prompt_1 = (
                        f"NOME DO ARQUIVO: {st.session_state.get('transcricao_nome_arquivo', 'nao_informado')}\n\n"
                        f"TRANSCRIÇÃO:\n{transcription_text}"
                    )
                    preview_text = call_model_text(PROMPT_1_PREVIA, contexto_prompt_1, max_tokens=3500)
                    st.session_state["preview_text"] = preview_text
                    st.success("Prévia gerada. Revise e edite antes de gravar no template.")
                except Exception as exc:
                    st.error(f"Falha ao gerar a prévia da ata: {exc}")

    if st.session_state.get("preview_text"):
        st.subheader("Prévia editável")
        st.caption("Texto puro para revisão humana antes da gravação no template.")
        edited_preview = st.text_area(
            "Prévia da ata",
            value=st.session_state["preview_text"],
            height=520,
            key="preview_editor",
        )
        st.session_state["preview_text"] = edited_preview
        render_guided_editor()

        with st.expander("Prompt 2 pronto para Copilot Word", expanded=False):
            prompt_2_completo = build_prompt_2_for_word(st.session_state["preview_text"])
            st.text_area(
                "Copie e cole no Copilot do Word com o template aberto",
                value=prompt_2_completo,
                height=380,
                disabled=True,
            )

    if st.button("2. Gravar no template", use_container_width=True):
        if not st.session_state.get("preview_text"):
            st.error("Gere ou edite a prévia da ata antes de gravar no template.")
        elif template_file is None:
            st.error("Carregue o template DOCX antes de gravar.")
        else:
            blueprint = st.session_state.get("template_blueprint")
            if blueprint is None:
                st.error("Não foi possível analisar o template carregado.")
            else:
                with st.spinner("Planejando e gravando no template..."):
                    try:
                        document, report = fill_template_by_spec(template_file.getvalue(), st.session_state["preview_text"])
                        st.session_state["generation_report"] = report

                        payload = preview_to_payload(st.session_state["preview_text"])
                        nome_arquivo = extrair_nome_arquivo(
                            payload["cliente"],
                            payload["data_reuniao"],
                            payload["horas"],
                        )

                        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
                            document.save(tmp.name)
                            with open(tmp.name, "rb") as file_handle:
                                file_bytes = file_handle.read()

                        st.success(f"Documento gerado: {nome_arquivo}")
                        st.download_button(
                            "Baixar ata",
                            data=file_bytes,
                            file_name=nome_arquivo,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            use_container_width=True,
                            type="primary",
                        )
                    except Exception as exc:
                        st.error(f"Falha ao gravar no template: {exc}")

    report = st.session_state.get("generation_report")
    if report:
        st.subheader("Resultado da gravação")
        st.text(
            f"Tabelas preenchidas: {report['tabelas_preenchidas']}\n"
            f"Linhas Convocados: {report['linhas_convocados']}\n"
            f"Linhas Pendências: {report['linhas_pendencias']}\n"
            f"Linhas Plano de Ação: {report['linhas_plano_acao']}"
        )

with tab2:
    st.text(
        "Como usar:\n\n"
        "1. Carregue a transcrição e o template real.\n"
        "2. Gere a prévia da ata em texto puro.\n"
        "3. Revise a prévia diretamente no editor ou na edição guiada.\n"
        "4. Grave no template.\n\n"
        "A gravação final segue a especificação estrutural do template EAS010-ATA-Template-v3."
    )