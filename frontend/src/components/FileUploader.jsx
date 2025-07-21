import React, {useEffect, useState} from 'react';
import Loading from "./Loading";
import FetchingError from "./FetchingError";
import DisplayJSON from "./DisplayJSON";

const FileUploader = ({type}) => {
  const [isFetching, setIsFetching] = useState(false);
  const [fetchedData, setFetchedData] = useState();
  const [errors, setErrors] = useState('');
  const [img, setImage] = useState();



  useEffect(() => {
    setIsFetching(false);
    setFetchedData();
    setErrors('');
    setImage();

  }, [type]);
  function handleImageChange(e) {
    setImage(e.target.files[0])
    setErrors('');
  }

  async function FetchData() {
    try {
      const path = type == 'tesseract' ? "http://127.0.0.1:8000/tesseract/extract" : "http://127.0.0.1:8000/llm/extract"
      const formData = new FormData();
      formData.append('file', img)
      setIsFetching(true)
      setErrors('')
      const response = await fetch(path, {
        method: 'POST',
        body: formData,
      })
      setIsFetching(false)
      if (!response.ok) {
        const errorBody = await response.json();
        setErrors("Something went wrong");

        return
      }
      const resData = await response.json()
      setFetchedData(resData)
    }catch (e) {
      setErrors("Something went wrong")
    }
     finally {
    setIsFetching(false);
    }


  }


  function handleSubmit(e) {
    setFetchedData();
    e.preventDefault();
    if(!img) {
      setErrors("Please Select An Image")
      return
    }

      FetchData();
    }



  return (
      <div className="bg-white shadow-md rounded-xl p-8 w-full max-w-2xl mx-auto mt-8">
        <form
            onSubmit={handleSubmit}

        >
          <h2 className="text-2xl font-bold text-red-600 ">{type==='tesseract' ? "Tesseract Base Extraction" : "LLM Base Extraction"}</h2>
          <p className="mb-6">{type==='tesseract' ? "Lower Latency, Lower Accuracy" : "Higher Latency, Higher Accuracy"} </p>
          <div className='pb-5'>
            <label
                htmlFor="fileInput"
                className="block text-sm font-medium text-gray-700 mb-1 pb-5"
            >
              Upload Image or PDF
            </label>
            <input
                id="fileInput"
                type="file"
                accept="image/*,.pdf"
                onChange={handleImageChange}

                className="block w-full border border-gray-300 rounded-md shadow-sm px-3 py-2 text-sm file:bg-red-600
          file:text-white file:border-none file:rounded file:px-4 file:py-2 hover:file:bg-red-700 transition"
            />
          </div>

          <button
              type="submit"
              className="bg-red-600 text-white font-semibold px-6 py-2 rounded-md hover:bg-red-700 transition"
          >
            Extract
          </button>

        </form>
        <div className='mt-3'>
          {errors && <FetchingError error={errors} />}
        </div>
        <div className='mt-3'>
          {isFetching && <Loading/>}
        </div>
        <div className='mt-3'>
          {fetchedData && <DisplayJSON data={fetchedData}/>}

        </div>
      </div>
  );
};

export default FileUploader;
