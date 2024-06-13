
function downloadReport(noteId) {
    fetch(`/download_report/${noteId}`)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            a.download = 'report.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
        })
        .catch(error => console.error('Error:', error));
}

function toggleGraph(index) {
    var graphs = document.getElementsByClassName("graph-img");
    for (var i = 0; i < graphs.length; i++) {
        if (i === index) {
            graphs[i].style.display = "block";
        } else {
            graphs[i].style.display = "none";
        }
    }
}
