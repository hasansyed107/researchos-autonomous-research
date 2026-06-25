import os
import streamlit as st
from datetime import datetime

from graph.workflow import workflow
from pdf_export import generate_pdf

from tools.pdf_loader import load_pdf
from tools.rag_pipeline import process_document


st.set_page_config(
    page_title="ResearchOS",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ResearchOS")
st.subheader("Multi-Agent AI Research System")


# ==================================================
# Sidebar - History
# ==================================================

st.sidebar.title("📚 Research History")

if os.path.exists("reports"):

    report_files = sorted(
        os.listdir("reports"),
        reverse=True
    )

    if report_files:

        selected_report = st.sidebar.selectbox(
            "Select Report",
            report_files
        )

        if st.sidebar.button(
            "Open Report"
        ):

            with open(
                f"reports/{selected_report}",
                "r",
                encoding="utf-8"
            ) as f:

                old_report = f.read()

            st.markdown(
                "## Previous Report"
            )

            st.markdown(
                old_report
            )

st.sidebar.markdown("---")
st.sidebar.title("🤖 Agent Logs")


# ==================================================
# Inputs
# ==================================================

query = st.text_input(
    "Enter Research Topic",
    placeholder="AI Coding Assistants"
)

uploaded_file = st.file_uploader(
    "Upload PDF (Optional)",
    type=["pdf"]
)


# ==================================================
# Generate Report
# ==================================================

if st.button("Generate Report"):

    if not query:

        st.warning(
            "Please enter a research topic."
        )

    else:

        rag_data = {
            "market_chunks": [],
            "technology_chunks": [],
            "trends_chunks": []
        }

        # ==================================================
        # PDF Processing
        # ==================================================

        if uploaded_file:

            pdf_text = load_pdf(
                uploaded_file
            )

            rag_data = process_document(
                pdf_text,
                query
            )

        # ==================================================
        # Workflow
        # ==================================================

        with st.spinner(
            "Running ResearchOS..."
        ):

            result = workflow.invoke(
                {
                    "query": query,

                    "market_chunks":
                    rag_data.get(
                        "market_chunks",
                        []
                    ),

                    "technology_chunks":
                    rag_data.get(
                        "technology_chunks",
                        []
                    ),

                    "trends_chunks":
                    rag_data.get(
                        "trends_chunks",
                        []
                    )
                }
            )

            # ==================================================
            # Results
            # ==================================================

            report = result.get(
                "report",
                "Report generation failed."
            )

            research_summary = result.get(
                "research_summary",
                ""
            )

            review = result.get(
                "review",
                ""
            )

            fact_check = result.get(
                "fact_check",
                ""
            )

            # Debug check

            print(
                "Summary Length:",
                len(
                    research_summary
                )
            )

            # ==================================================
            # Save Report
            # ==================================================

            os.makedirs(
                "reports",
                exist_ok=True
            )

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            report_path = (
                f"reports/report_{timestamp}.md"
            )

            with open(
                report_path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(report)

            pdf_file = generate_pdf(
                report
            )

        # ==================================================
        # Main Output
        # ==================================================

        st.success(
            "✅ Research Complete!"
        )

        st.info(
            f"Saved to: {report_path}"
        )

        st.markdown(
            "## Research Report"
        )

        st.markdown(
            report
        )

        # ==================================================
        # Sidebar Logs
        # ==================================================

        with st.sidebar.expander(
            "📋 Research Summary"
        ):
            st.write(
                research_summary
            )

        with st.sidebar.expander(
            "📝 Review Notes"
        ):
            st.write(
                review
            )

        with st.sidebar.expander(
            "✅ Fact Check"
        ):
            st.write(
                fact_check
            )

        # ==================================================
        # Downloads
        # ==================================================

        with open(
            pdf_file,
            "rb"
        ) as pdf:

            st.download_button(
                label="📄 Download PDF Report",
                data=pdf,
                file_name="report.pdf",
                mime="application/pdf"
            )

        st.download_button(
            label="📝 Download Markdown Report",
            data=report,
            file_name="report.md",
            mime="text/markdown"
        )