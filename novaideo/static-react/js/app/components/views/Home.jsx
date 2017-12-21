import React from 'react';
import SwipeableViews from 'react-swipeable-views';
import AppBar from 'material-ui/AppBar';
import Tabs, { Tab } from 'material-ui/Tabs';
import Typography from 'material-ui/Typography';
import { connect } from 'react-redux';

import IdeasList from '../idea/IdeasList';

function TabContainer({ children }) {
  return (
    <Typography component="div" style={{ padding: 8 * 3 }}>
      {children}
    </Typography>
  );
}

class Home extends React.Component {
  state = {
    value: 1
  };

  handleChange = (event, value) => {
    this.setState({ value: value });
  };

  handleChangeIndex = (index) => {
    this.setState({ value: index });
  };

  render() {
    return (
      <div>
        <AppBar position="static" color="default">
          <Tabs
            value={this.state.value}
            onChange={this.handleChange}
            indicatorColor="primary"
            textColor="primary"
            fullWidth
            centered
          >
            <Tab label="Questions" />
            <Tab label="Ideas" />
            <Tab label="Proposals" />
          </Tabs>
        </AppBar>
        <SwipeableViews index={this.state.value} onChangeIndex={this.handleChangeIndex}>
          <TabContainer>Questions</TabContainer>
          <TabContainer>
            {this.state.value === 1 && <IdeasList />}
          </TabContainer>
          <TabContainer>Proposals</TabContainer>
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