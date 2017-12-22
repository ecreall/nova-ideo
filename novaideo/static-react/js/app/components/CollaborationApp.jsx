import React from 'react';

import Navbar from './Navbar';
import Footer from './Footer';
import App from './common/App';

function CollaborationApp({ children, active, left }) {
  return (
    <App active={active} left={left} Navbar={Navbar}>
      {children}
      <Footer />
    </App>
  );
}

export default CollaborationApp;