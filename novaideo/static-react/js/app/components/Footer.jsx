import React from 'react';
import { connect } from 'react-redux';

import { STICKER_MAN_1 } from '../constants';

class Footer extends React.Component {
  render() {
    return (
      <div fluid className="background-dark relative" id="footer">
        <img alt="Sticker" style={{ width: 150, height: 150 }} src={STICKER_MAN_1} />
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {};
};

export default connect(mapStateToProps)(Footer);