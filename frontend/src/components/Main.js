import React, {useState, useEffect} from 'react'

const Main = () => {
    const [centers, setCenters] = useState(0);
    const [manpower, setManpower] = useState(0);

    return (
        <div class='main__prompt'>
            <h2>evaluate optimal centre locations</h2>
            <form>
                <label>number of centers to allocate</label>
                <input type='number' name='centers' value={centers} onChange={e => setCenters(e.target.value)}/>
                <br />
                <label>number of healthcare workers available</label>
                <input type='number' name='manpower' value={manpower} onChange={e => setManpower(e.target.value)}/>
                <button>RUN</button>
            </form>
        </div>
    )
}

export default Main