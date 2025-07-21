import {useState} from "react";
import FetchingError from "./FetchingError";
import SuccessNotif from "./SuccessNotif";


const DisplayJSON = ({data}) => {
    const [errors, setErrors] = useState();
    const [savedSuccessfully, setSavedSuccessfully] = useState(false)
    function handleDownload() {
    const jsonStr = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);

    const a = document.createElement('a');
    a.href = url;
    a.download = 'extracted_data.json';
    a.click();
    URL.revokeObjectURL(url);
    }

    async function handleSaveToDB(){
        setErrors();
        setSavedSuccessfully(false);
        try{
            const path = "http://127.0.0.1:8000/invoices"
            const res = await fetch(path, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body : JSON.stringify(data)
        })
            if (!res.ok) {
            const errorBody = await res.json();

            if (res.status === 422) {
                setErrors("We couldn't extract data compatible with the database.");
            } else if (errorBody.detail) {
                setErrors(errorBody.detail);
            } else {
                setErrors("Something went wrong with the DB.");
            }

            return;
        }
        setSavedSuccessfully(true)
        } catch(e) {
            setErrors("Something went wrong with the DB");
        }
    }



    return (
        <>
            <div className="bg-gray-900 text-gray-100 rounded-xl overflow-hidden shadow-lg max-w-3xl mx-auto">
                <div className="bg-red-600 text-xs uppercase px-4 py-2 font-bold tracking-wide text-white">
                    json
                </div>
                <pre className="text-sm p-4 overflow-x-auto whitespace-pre-wrap break-words">
                <code className="language-json">
                    {JSON.stringify(data)}
                </code>
            </pre>
            </div>

            <div className="px-4 py-3 flex ">
                <button
                    onClick={handleDownload}
                    className="bg-red-600 text-white font-semibold px-6 py-2 rounded-md hover:bg-red-700 transition mr-5">
                    Download JSON
                </button>
                <button
                    onClick={handleSaveToDB}
                    className="bg-red-600 text-white font-semibold px-6 py-2 rounded-md hover:bg-red-700 transition">
                    Save JSON To Database
                </button>
            </div>

            <div className='mt-4'>
                {
                    errors && <FetchingError error={errors}/>
                }
            </div>
            <div className='mt-4'>
                {
                    savedSuccessfully && <SuccessNotif message="Data saves successfully!" />
                }
            </div>
        </>
    )

}

export default DisplayJSON;