const API_BASE = "https://foto-owl-api.onrender.com";

async function startImport() {
  const link = document.getElementById("link").value.trim();
  const out = document.getElementById("out");

  if (!link) {
    out.innerText = "Please paste a Google Drive folder link.";
    return;
  }

  out.innerText = "Importing images... please wait";

  try {
    const res = await fetch(`${API_BASE}/import`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ folder_url: link })
    });

    const data = await res.json();

    if (!res.ok) {
      out.innerText = "Import failed. Check backend logs.";
      return;
    }

    out.innerText = `Images imported successfully: ${data.images}`;
    loadImages();
  } catch (err) {
    out.innerText = "Server error while importing.";
    console.error(err);
  }
}

async function loadImages() {
  const list = document.getElementById("images");
  list.innerHTML = "Loading images...";

  try {
    const res = await fetch(`${API_BASE}/images`);
    const imgs = await res.json();

    list.innerHTML = "";

    if (imgs.length === 0) {
      list.innerText = "No images imported yet.";
      return;
    }

    imgs.forEach(name => {
      const div = document.createElement("div");
      div.innerText = name;
      list.appendChild(div);
    });
  } catch (err) {
    list.innerText = "Unable to load images.";
  }
}
