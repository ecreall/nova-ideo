import React from 'react';
import { connect } from 'react-redux';

import Record from './forms/widgets/Record';

class Footer extends React.Component {
  render() {
    return (
      <div fluid className="background-dark relative" id="footer">
        <Record />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {};
};

export default connect(mapStateToProps)(Footer);