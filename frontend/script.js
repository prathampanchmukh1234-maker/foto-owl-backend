async function importImages() {
  const url = document.getElementById("folderUrl").value;

  if (!url) {
    alert("Please enter a Google Drive folder URL");
    return;
  }

  try {
    const response = await fetch("http://localhost:8000/import/google-drive", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        folder_url: url
      })
    });

    if (!response.ok) {
      throw new Error("Failed to start import");
    }

    const data = await response.json();

    alert(`Import started. Images queued: ${data.images}`);
  } catch (error) {
    console.error(error);
    alert("Error starting import. Check backend logs.");
  }
}
