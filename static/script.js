
    document.addEventListener('DOMContentLoaded', function () {
        const uploadForm = document.getElementById('uploadForm');
        const downloadForm = document.getElementById('downloadForm');
        const downloadKeyInput = document.getElementById('downloadKeyInput');

        uploadForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const formData = new FormData(uploadForm);
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData,
            });

            const result = await response.json();
            if (result.success) {
                alert(`File uploaded successfully with key: ${result.key}`);
            } else {
                alert(result.message);
            }
        });

        downloadForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const key = downloadKeyInput.value.trim();
            if (key) {
            
                try {
                    const checkKeyResponse = await fetch(`/check_key/${key}`);
                    const checkKeyResult = await checkKeyResponse.json();
                    const checkKeyResponseText = await checkKeyResponse.text();
                        console.log('Check Key Response:', checkKeyResponseText);
                    console.log('Check Key Result:', checkKeyResult);    
                    if (checkKeyResult.valid) {
                        const downloadResponse = await fetch(`/download/${key}`);
                        if (downloadResponse.ok) {
                            const blob = await downloadResponse.blob();
                            const link = document.createElement('a');
                            link.href = window.URL.createObjectURL(blob);
                            link.download = key;
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                        } else {
                            const errorResponse = await downloadResponse.json();
                            alert(errorResponse.message || 'Error downloading file.');
                        }
                    } else {
                        alert('Invalid key. Please enter a valid key.');
                    }
                } catch (error) {
                    console.error('Error handling download:', error);
                    alert('Error handling download.');
                }
            } else {
                alert('Please enter a valid key.');
            }
        });
    });

