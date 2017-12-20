import React from 'react';
import AppBar from 'material-ui/AppBar';
import { connect } from 'react-redux';

class NavBar extends React.Component {
  render() {
    return <AppBar title="My AppBar" />;
  }
}

const mapStateToProps = (state) => {
  return {};
};

export default connect(mapStateToProps)(NavBar);