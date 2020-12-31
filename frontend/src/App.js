import Search from './components/Search'
import Dashboard from './components/Dashboard'
import Map from './components/Map'
import './styles/app.scss'
import logo from './assets/mediloc-logo.svg'

function App() {
  	return (
    	<div className='app'>
			<div className='app__tab'>
				<img src={logo} alt="Mediloc Logo"/>
				<Search />
				<Dashboard />
			</div>
			<Map />
    	</div>
  	);
}

export default App;
