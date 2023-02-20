import React from 'react';
import '../styles/LendingPage.css';
import face from '../images/face.svg';
import logo from '../images/logo_main.svg';
import elements from '../images/elements.svg';
import triangle from '../images/triangle.svg';


const Logo = () => (<img src={logo} className={'logo'} alt='logo'/>);

const Face = () => (<img src={face} className={'face'} alt='face'/>);

const Elements = () => (<img src={elements} className={'elements'} alt='elements'/>);

const Triangle = () => (<img src={triangle} className={'triangle'} alt='triangle'/>);


const LendingPage = () => {
  return (
    <div className='LendingPage'>
        <div>
        <Logo />
        </div>

      <div>
        <Face />
        <Elements />
        <Triangle />
      </div>
    </div>
  );
};

export default LendingPage;