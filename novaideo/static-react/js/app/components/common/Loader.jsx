import React from 'react';
import { Translate } from 'react-redux-i18n';
import Ellipsis from '../svg/ellipsis';

const Loader = ({ textHidden, color }) => {
  return (
    <div className={textHidden ? 'loader-container-xs' : 'loader-container-xl'}>
      <div className="loader">
        {!textHidden && <Translate value="loading.wait" />}
        <div className="relative">
          <Ellipsis color={color} />
        </div>
      </div>
    </div>
  );
};

export default Loader;