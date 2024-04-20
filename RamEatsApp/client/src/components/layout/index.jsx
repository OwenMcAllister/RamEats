import { Outlet } from 'react-router-dom'
import './index.scss'
import Navbar from '../navbar'
import Topbar from '../topbar'

const Layout = () => {
    return (
        <div className='App'>
            <Topbar />
            <Outlet />
            <Navbar />
        </div>
    )
}

export default Layout