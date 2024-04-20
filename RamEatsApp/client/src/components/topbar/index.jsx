import logo from '../../assets/RamEatsLogo.svg'
import './index.scss'

const Topbar = () => {
    return (
        <>
            <div className='topbar'>
                <h1>RamEats</h1>
                <img src={logo} alt='logo' height={'50px'}/>
            </div>
        </>
    );

}

export default Topbar