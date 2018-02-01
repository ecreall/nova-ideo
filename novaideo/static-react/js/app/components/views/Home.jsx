import React from 'react';
import Typography from 'material-ui/Typography';
import { connect } from 'react-redux';

import IdeasList from '../idea/IdeasList';
import CreateIdeaForm from '../forms/CreateIdea';
import Idea from '../idea/Idea';
import { updateApp } from '../../actions/actions';

function TabContainer({ children }) {
  return (
    <Typography
      component="div"
      style={{
        marginTop: 25,
        maxWidth: 588,
        marginLeft: 'auto',
        marginRight: 'auto'
      }}
    >
      {children}
    </Typography>
  );
}

class Home extends React.Component {
  constructor(props) {
    super(props);
    this.openChannel(this.props.params.channelId || null);
  }

  state = {
    value: 1
  };

  openChannel = (channelId) => {
    if (channelId) {
      const { smallScreen } = this.props;
      this.props.updateApp('chatApp', {
        drawer: !smallScreen,
        open: true,
        channel: channelId
      });
    }
  };

  handleChange = (event, value) => {
    this.setState({ value: value });
  };

  handleChangeIndex = (index) => {
    this.setState({ value: index });
  };

  render() {
    const value = this.state.value;
    const { ideaId } = this.props.params;
    return (
      <div>
        {ideaId && <Idea id={ideaId} open />}
        {value === 0 && <TabContainer>Questions</TabContainer>}
        {value === 1 &&
          <TabContainer>
            <CreateIdeaForm />
            <IdeasList />
          </TabContainer>}
        {value === 2 && <TabContainer>Proposals</TabContainer>}
      </div>
    );
  }
}

export const mapDispatchToProps = {
  updateApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    smallScreen: state.globalProps.smallScreen
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(Home);