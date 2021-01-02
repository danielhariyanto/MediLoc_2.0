import React from 'react'
import '../styles/search.scss'

const Search = () => {
    return (
        <form className='search'>
            <input type='text' name='query' placeholder='Search City' />
        </form>
    )
}

export default Search