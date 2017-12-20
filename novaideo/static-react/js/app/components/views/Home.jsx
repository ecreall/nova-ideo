import React from 'react';
import { Tabs, Tab } from 'material-ui/Tabs';
import SwipeableViews from 'react-swipeable-views';
import { connect } from 'react-redux';

import IdeasList from '../idea/IdeasList';

const styles = {
  headline: {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400
  },
  slide: {
    padding: 10
  }
};

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      slideIndex: 0
    };
  }

  handleChange = (value) => {
    this.setState({
      slideIndex: value
    });
  };

  render() {
    return (
      <div className="home">
        <Tabs onChange={this.handleChange} value={this.state.slideIndex}>
          <Tab label="Ideas" value={0} />
          <Tab label="Questions" value={1} />
          <Tab label="Proposals" value={2} />
        </Tabs>
        <SwipeableViews index={this.state.slideIndex} onChangeIndex={this.handleChange}>
          <div>
            <IdeasList />
          </div>
          <div style={styles.slide}>questions</div>
          <div style={styles.slide}>proposals</div>
        </SwipeableViews>
      </div>
    );
  }
}

const mapStateToProps = (state) => {
  return {
    i18n: state.i18n
  };
};

export default connect(mapStateToProps)(Home);