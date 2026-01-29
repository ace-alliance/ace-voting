# ace-voting

## How to create the metadata file

This guide explains how to generate and commit the rationale metadata file for a Governance Action (GA).

### Prerequisites
- Access to the internal Google Doc containing the voting rationale.
- Git installed and configured.

### Step-by-Step Instructions

#### 1. Prepare the Rationale Content
1. Open the Google Doc containing the rationale text.
2. Download the document content as Markdown or keep it open to copy-paste sections.
   - *Note: Ensure you have the Summary, Rationale Statement, Precedent Discussion, Counterargument Discussion, and Conclusion ready.*

#### 2. Generate Metadata JSON
1. Navigate to the **Cardano Foundation Voting Tool**: [voting.cardanofoundation.org](https://voting.cardanofoundation.org)
2. **Select the Governance Action**:
   - Find the specific Governance Action you are voting on (verify the Gov Action ID).
3. **Fill out the Information**:
   - Copy the text from your source document into the corresponding fields in the tool:
     - **Summary**
     - **Rationale Statement**
     - **Precedent Discussion**
     - **Counterargument Discussion**
     - **Conclusion**
   - Ensure specific references (like Constitution and Governance Action Metadata) are included if part of the rationale.
4. **Download**:
   - Once filled, click the download button to get the JSON file containing the rationale.

#### 3. Rename and Organize
1. Locate the downloaded file.
2. **Rename the file** following the repository's naming convention:
   - Format: `ga<Index>-<Short-Description>.json`
   - Example: `ga84-van-rossem-hf.json`
   - *Tip: Look at existing files in the directory to match the `ga` numbering sequence.*
3. Move the file into the correct folder in this repository (e.g., `202601/` for January 2026).

#### 4. Commit and Push
1. Open your terminal or Git client in the repository folder.
2. Run the following commands:
   ```bash
   git pull origin main             # Ensure you have the latest changes
   git add <path/to/your/file>      # e.g., git add 202601/ga84-van-rossem-hf.json
   git commit -m "Add rationale for GA<Index>"
   git push origin main
   ```

#### 5. Share with Team
1. Go to the file in the GitHub repository interface.
2. Click the **"Raw"** button to view the raw JSON content.
3. Copy the URL from the browser address bar.
4. Share this **Raw URL** in the team chat.
