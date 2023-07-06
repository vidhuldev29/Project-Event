ClassicEditor
                .create( document.querySelector( '#editor' ), {
                    ckbox: {
                        tokenUrl: 'https://your.token.url',
                    },
                    toolbar: [
                        'ckbox', 'imageUpload', '|', 'heading', '|', 'undo', 'redo', '|', 'bold', 'italic', '|',
                        'blockQuote', 'indent', 'link', '|', 'bulletedList', 'numberedList'
                    ],
                } )
                .catch( error => {
                    console.error( error );
                } );