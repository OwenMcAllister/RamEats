import { Outlet } from 'react-router-dom'
import logo from '../../../assets/RamEatsLogo.svg'
import './index.scss'

const OnboardingLayout = () => {
    return (
        <div className='App'>
            <ul>
            <img src={logo} alt='Logo' height={'50px'}/>
                <h1>RamEats</h1> 
                <h2>Welcome!</h2>
                <p>Complete these steps to get started.</p>
                <form>
                    <Outlet />
                </form>
            </ul>
        </div>
    )
}

export default OnboardingLayout