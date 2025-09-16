# app.py
import streamlit as st
import pandas as pd
import tempfile
import os
from pathlib import Path


# Import backend functions
# from .backend import (
#     extract_text_from_pdf, 
#     search_keywords_in_text,
#     process_pdf_with_keywords, 
#     get_default_keywords,
#     load_keywords,
#     save_keywords,
#     get_keywords_file_path)

from backend import (
    extract_text_from_pdf, 
    search_keywords_in_text,
    process_pdf_with_keywords, 
    get_default_keywords,
    load_keywords,
    save_keywords,
    get_keywords_file_path)

from image_setting import show_logo


# Set page configuration
st.set_page_config(
    page_title="Smart Search",
    page_icon="🔍",
    layout="wide",
)

# Load external CSS
def load_css():
    """Load CSS from the package directory"""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Call it once at the beginning of your app
# load_css("styles.css")
load_css()


if 'keywords_list' not in st.session_state:
    st.session_state.keywords_list = load_keywords()

# ------


def main():
    # st.title("Smart Search")
    # st.markdown("Search for keywords in PDF documents")

    with st.container(key = "main"):
        # st.markdown('<h1 class="custom-title">Smart Search</h1>', unsafe_allow_html=True)
        # st.markdown('<p class="center-text">Search for keywords in PDF documents</p>', unsafe_allow_html=True)
        # st.title("Smart Search")
        # st.markdown("Search for keywords in PDF documents")

        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            logo_html = show_logo(
                Path(__file__).parent / "logo.png", 
                width=400
            )
            st.markdown(logo_html, unsafe_allow_html=True)
            
            # st.markdown("Search for keywords in PDF documents")
            st.markdown("""
                <p style="
                    font-family: 'Work Sans', sans-serif;
                    letter-spacing: 0.15em;
                    margin-bottom: 1rem;
                    font-weight:500;
                ">
                    Search for keywords in PDF documents
                </p>
            """, unsafe_allow_html=True)

        

        # Creating two columns
        pdf_uploader, keyword_section = st.columns(2)

        # Left: The PDF Uploader
        # 1. PDF Selection/Upload
        with pdf_uploader:
            st.subheader("Select PDF File")
            uploaded_pdf = st.file_uploader(
                "Upload a PDF file", 
                type="pdf",
                help="Choose a PDF file to analyze"
            )
        
            if uploaded_pdf:
                st.success(f"Selected: {uploaded_pdf.name}")

        
        
        # Right: Keyword Management section
        # 2. Keywords Management Section
        with keyword_section:
            st.subheader("Manage Keywords")

            # Add the Collapsible Section
            st.text("Expand the section to manage keywords")
            with st.expander("Keywords Management Section", 
                            expanded=False):
                
                # Show total keywords count at the top
                total_keywords = len(st.session_state.keywords_list) if 'keywords_list' in st.session_state else 0
                st.info(f"**Total current keywords: {total_keywords}**")
        
                # Search/Filter box with quick add functionality - More responsive version
                search_col, add_col, clear_col = st.columns([7, 2, 1])
                
                with search_col:
                    # Using st.text_input with auto-rerun for better responsiveness
                    if 'search_counter' not in st.session_state:
                        st.session_state.search_counter = 0
                    
                    search_term = st.text_input(
                        "Search",
                        placeholder="🔍 Search keywords or type to add new...",
                        key=f"keyword_search_{st.session_state.search_counter}",
                        label_visibility="collapsed"
                    )
                    
                    # Store search term in session state for persistence
                    if 'current_search' not in st.session_state:
                        st.session_state.current_search = ""
                    
                    # Update current search if it changed
                    if search_term != st.session_state.current_search:
                        st.session_state.current_search = search_term
                        # Force rerun for dynamic filtering
                        st.rerun()
                    
                    # Use the stored search term for consistency
                    search_term = st.session_state.current_search
                
                # Filter keywords based on search term
                filtered_keywords = []
                original_indices = []  # Keep track of original indices for removal
                
                if st.session_state.keywords_list:
                    if search_term.strip():
                        # Filter keywords that contain the search term (case insensitive)
                        for i, keyword in enumerate(st.session_state.keywords_list):
                            if search_term.lower() in keyword.lower():
                                filtered_keywords.append(keyword)
                                original_indices.append(i)
                    else:
                        # Show all keywords when no search term
                        filtered_keywords = st.session_state.keywords_list.copy()
                        original_indices = list(range(len(st.session_state.keywords_list)))
                
                # Check if search term exists in keywords (exact match, case insensitive)
                search_exists = search_term.strip().lower() in [kw.lower() for kw in st.session_state.keywords_list] if search_term.strip() else True
                
                # Show "Add" button if search term doesn't exist and is not empty
                with add_col:
                    if search_term.strip() and not search_exists:
                        if st.button(f"➕ Add", key="quick_add", help=f"Add '{search_term.strip()}'"):
                            st.session_state.keywords_list.append(search_term.strip())
                            # Clear search term after adding
                            st.session_state.current_search = ""
                            st.session_state.search_counter += 1
                            st.rerun()

                # Clear search button
                with clear_col:
                    if search_term.strip():  # Only show clear button when there's text to clear
                        if st.button("🗑️", key="clear_search", help="Clear search"):
                            st.session_state.current_search = ""
                            st.session_state.search_counter += 1
                            st.rerun()
                
                
                # Scrollable box showing filtered keywords
                keywords_display = st.container(height=200)
                with keywords_display:
                    if filtered_keywords:
                        for display_index, (keyword, original_index) in enumerate(zip(filtered_keywords, original_indices)):
                            col_key, col_button = st.columns([8, 1])
                            with col_key:
                                # Show keyword with search term highlighted (basic text highlighting)
                                if search_term.strip():
                                    st.write(f"{display_index+1}. {keyword} *(contains '{search_term}')*")
                                else:
                                    st.write(f"{display_index+1}. {keyword}")
                            with col_button:
                                if st.button("❌", key=f"remove_{original_index}_{display_index}", help=f"Remove '{keyword}'"):
                                    st.session_state.keywords_list.pop(original_index)
                                    # Clear search to refresh the view
                                    st.session_state.current_search = ""
                                    st.session_state.search_counter += 1
                                    st.rerun()

                    elif st.session_state.keywords_list and search_term.strip():
                        # Show message when no results found but keywords exist
                        st.write("*No keywords match your search*")
                    elif not st.session_state.keywords_list:
                        st.write("*No keywords added yet*")

                # Action buttons
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Clear All", key = "clear_button"):
                        st.session_state.keywords_list = []
                        st.rerun()
                
                with col_btn2:
                    if st.button("Reset to Default", key="reset_button"):
                        st.session_state.keywords_list = get_default_keywords()
                        st.rerun()


                # Add bulk input counter for unique keys
                if 'bulk_input_counter' not in st.session_state:
                    st.session_state.bulk_input_counter = 0

                bulk_keywords = st.text_area(
                    "Add multiple (one per line):", 
                    placeholder="keyword1\nkeyword2\nkeyword3",
                    height=120,
                    key=f"bulk_input_{st.session_state.bulk_input_counter}"
                )

                
                if st.button("Add All", key = "add_all_button"):
                    if bulk_keywords.strip():
                        new_keywords = [kw.strip() for kw in bulk_keywords.split('\n') if kw.strip()]
                        added_count = 0

                        # Create lowercase version of existing keywords for case-insensitive comparison
                        existing_keywords_lower = [kw.lower() for kw in st.session_state.keywords_list]

                        for kw in new_keywords:
                            # if kw not in st.session_state.keywords_list:
                            # Check if keyword already exists (case-insensitive)
                            if kw.lower() not in existing_keywords_lower:
                                st.session_state.keywords_list.append(kw)

                                existing_keywords_lower.append(kw.lower())  # Add to comparison list

                                added_count += 1
                        if added_count > 0:
                            st.success(f"Added {added_count} new keywords")
                            st.session_state.bulk_input_counter += 1  # Clear textarea
                            st.rerun()
                        else:
                            st.warning("Keyword already exists!")


                # Added Save Keywords functionality
                if st.button("Save Keywords", key = "save_keywords"):
                    if save_keywords(st.session_state.keywords_list):
                        filepath = get_keywords_file_path()
                        st.success(f"Keywords saved successfully!\nSaved keywords file: `{filepath}`")
                    else:
                        st.error("Failed to save keywords")
                
    # 3. Run Search Button
        can_run = uploaded_pdf is not None and len(st.session_state.keywords_list) > 0
        
        if not can_run:
            if not uploaded_pdf:
                st.warning("Please upload a PDF file first")
            if len(st.session_state.keywords_list) == 0:
                st.warning("Please add at least one keyword")
        
        search_button = st.button(
            "SEARCH", 
            type="primary", 
            disabled=not can_run,
            width="content",
            key = "search_button"
        )
        
        # 4. Results Section
        if search_button and can_run:
            st.subheader("Results")
            
            with st.spinner("Searching PDF for keywords..."):
                # Save PDF temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_pdf.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    # Use backend function to process PDF
                    pdf_text, results = process_pdf_with_keywords(
                        tmp_file_path, 
                        st.session_state.keywords_list
                    )
                    
                    if results:
                        # Summary metrics
                        col1, col2, col3 = st.columns(3)
                        # with col1.container(key="metric1"):
                        #     st.metric("Keywords Found", len(results))
                        with col1:
                            st.markdown(f"""
                                <div class="custom-metric-box">
                                    <div class="metric-label">Keywords Found</div>
                                    <div class="metric-value">{len(results)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with col2:
                            total_occurrences = sum(info['count'] for info in results.values())
                            # st.metric("Total Occurrences", total_occurrences)
                            st.markdown(f"""
                                <div class="custom-metric-box">
                                    <div class="metric-label">Total Occurrences</div>
                                    <div class="metric-value">{total_occurrences}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        with col3:
                            all_pages = set()
                            for info in results.values():
                                all_pages.update(info['pages'])
                            # st.metric("Pages with Results", len(all_pages))
                            st.markdown(f"""
                                <div class="custom-metric-box">
                                    <div class="metric-label">Pages with Results</div>
                                    <div class="metric-value">{len(all_pages)}</div>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        st.write("")  # Space
                        
                        # Results table
                        st.write("**Detailed Results:**")
                        
                        results_data = []
                        for keyword, info in results.items():
                            pages_str = ", ".join(map(str, info['pages']))
                            results_data.append({
                                'Keyword': keyword,
                                'Count': info['count'],
                                'Pages': pages_str
                            })
                        
                        df = pd.DataFrame(results_data)
                        df = df.sort_values('Count', ascending=False).reset_index(drop=True)
                        
                        st.dataframe(
                            df,
                            width="stretch",
                            hide_index=True,
                            column_config={
                                "Keyword": st.column_config.TextColumn("Keyword"),
                                "Count": st.column_config.NumberColumn("Count"),
                                "Pages": st.column_config.TextColumn("Pages Found")
                            }
                        )

                        
                        # Show keywords that weren't found
                        found_keywords = set(results.keys())
                        not_found = [kw for kw in st.session_state.keywords_list if kw not in found_keywords]
                        
                        if not_found:
                            with st.expander(f"Keywords Not Found ({len(not_found)})"):
                                st.write(", ".join(not_found))
                    
                    else:
                        st.error("❌ No keywords were found in the PDF")
                        st.info("💡 Try different keywords or check if the PDF contains searchable text")
                        
                        # Show all keywords that weren't found
                        with st.expander("🔍 Searched Keywords"):
                            st.write(", ".join(st.session_state.keywords_list))
                
                except Exception as e:
                    st.error(f"❌ Error processing PDF: {str(e)}")
                
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
                    


if __name__ == "__main__":
    main()