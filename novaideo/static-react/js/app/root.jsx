import React from 'react';
/*
  Parent class of all of Assembl. All high level components that require
  to exist in every context should be placed here. Eg. Alert, Modal, etc.
*/
export default ({ children }) => {
  return (
    <div>
      <div className="root-child">
        {children}
      </div>
    </div>
  );
};