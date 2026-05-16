import streamlit as st
from transformers import pipeline

# ── Konfiguracja strony ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="EN → DE Translator",
    page_icon="🌍",
    layout="centered",
)

# ── Tytuł i opis ─────────────────────────────────────────────────────────────
st.title("🌍 English → German Translator")
st.markdown(
    """
    Aplikacja umożliwia tłumaczenie tekstu z **języka angielskiego** na **język niemiecki**
    przy użyciu modelu językowego udostępnionego przez [Hugging Face](https://huggingface.co).

    ---
    ### 📋 Instrukcja
    1. Wpisz lub wklej tekst w języku angielskim w pole poniżej.
    2. Kliknij przycisk **Tłumacz**.
    3. Przetłumaczony tekst pojawi się w sekcji wyników.

    > ⚠️ Przy pierwszym uruchomieniu model musi zostać pobrany — może to chwilę potrwać.
    """
)

st.divider()

# ── Ładowanie modelu (cache) ──────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_translator():
    return pipeline("translation_en_to_de", model="Helsinki-NLP/opus-mt-en-de")

# ── Interfejs użytkownika ─────────────────────────────────────────────────────
input_text = st.text_area(
    label="✏️ Tekst do przetłumaczenia (angielski)",
    placeholder="Enter English text here...",
    height=180,
)

translate_btn = st.button("🔄 Tłumacz", use_container_width=True)

# ── Logika tłumaczenia ────────────────────────────────────────────────────────
if translate_btn:
    if not input_text.strip():
        st.warning("⚠️ Pole tekstowe jest puste. Wpisz tekst przed tłumaczeniem.")
    else:
        with st.spinner("⏳ Trwa tłumaczenie... proszę czekać."):
            try:
                translator = load_translator()
                result = translator(input_text, max_length=512)
                translated = result[0]["translation_text"]

                st.success("✅ Tłumaczenie zakończone pomyślnie!")
                st.subheader("🇩🇪 Wynik tłumaczenia")
                st.text_area(
                    label="Przetłumaczony tekst (niemiecki)",
                    value=translated,
                    height=180,
                )

                # Przycisk kopiowania przez download
                st.download_button(
                    label="💾 Pobierz wynik jako .txt",
                    data=translated,
                    file_name="tlumaczenie_de.txt",
                    mime="text/plain",
                )

            except Exception as e:
                st.error(f"❌ Wystąpił błąd podczas tłumaczenia: {e}")

# ── Stopka ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Model: Helsinki-NLP/opus-mt-en-de | Powered by Hugging Face Transformers & Streamlit")
st.caption("Numer indeksu: s21871")
