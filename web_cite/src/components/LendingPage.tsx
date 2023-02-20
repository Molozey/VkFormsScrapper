import React from 'react';
import '../styles/LendingPage.css';
import face from '../images/face.svg';
import logo from '../images/Logo.png';
import elements from '../images/elements.svg';
import triangle from '../images/triangle.svg';


function Logo(svg: any) {
  return (
      <img src={svg} className={'logo'} alt='Logo'/>
  );
}

const Face = (svg: any) => {
  return (
      <img src={svg} className={'face'} alt='Face' />
  );
};

const Elements = (svg: any) => {
  return <img src={svg} className={'elements'} alt='Elements' />
};

const Triangle = (svg: any) => {
  return (
      <img src={svg} className={'triangle'} alt='Triangle'/>
  )
};


const LendingPage = () => {
  return (
    <div className={'LendingPage'}>
        <div>
        <Logo svg={logo} />
        </div>

      <div>
        <Face svg={face}/>
        <Elements svg={elements}/>
        <Triangle svg={triangle}/>
      </div>

    </div>
  );
};

export default LendingPage;