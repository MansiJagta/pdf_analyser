import UploadDropzone from "../components/UploadDropzone";

export default function Upload() {
    const handleFilesSelected = (files) => {
        console.log("Files selected:", files);
        // Logic to upload/store files would go here
    };

    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in">
            <div className="text-center space-y-2">
                <h1 className="text-3xl font-bold text-white">Upload Documents</h1>
                <p className="text-text-muted">
                    Add your PDF or Image files to start analyzing.
                </p>
            </div>

            <div className="bg-surface/30 backdrop-blur-sm border border-surface rounded-2xl p-6 sm:p-10 shadow-xl">
                <UploadDropzone onFilesSelected={handleFilesSelected} />
            </div>
        </div>
    );
}
