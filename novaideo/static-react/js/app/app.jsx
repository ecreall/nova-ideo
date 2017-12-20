import React from 'react';
import Navbar from './components/Navbar';
import Footer from './components/Footer';

class App extends React.Component {
  render() {
    return (
      <div className="app-container">
        <Navbar />
        <div className="app-content">
          <div className="app">
            <div className="app-child">
              {this.props.children}
            </div>
          </div>
        </div>
        <Footer />
      </div>
    );
  }
}

export default App;