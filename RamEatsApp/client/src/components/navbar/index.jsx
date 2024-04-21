import { NavLink } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCog, faHome } from '@fortawesome/free-solid-svg-icons';
import './index.scss'

const Navbar = () => {

    return (
        <>
            <div className='bottom-nav'>
                <nav>
                    <NavLink
                        exact="true"
                        activeclassname="active"
                        to="/"
                    >
                        <FontAwesomeIcon icon={faHome} color="#000" />
                    </NavLink>
                    <NavLink
                        activeclassname="active"
                        to="/settings"
                    >
                        <FontAwesomeIcon icon={faCog} color="#000" />
                    </NavLink>
                </nav>
            </div>
        </>
    )
}

export default Navbar