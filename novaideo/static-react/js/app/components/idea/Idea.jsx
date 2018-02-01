/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { browserHistory } from 'react-router';

import { ideaQuery } from '../../graphql/queries';
import Dialog from '../common/Dialog';
import { updateApp } from '../../actions/actions';

export class DumbIdea extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      open: this.props.open
    };
  }

  close = () => {
    this.setState({ open: false }, () => {
      const { previousLocation } = this.props;
      if (previousLocation) {
        browserHistory.replace(previousLocation);
      } else {
        browserHistory.replace('/');
      }
    });
  };

  render() {
    const { idea } = this.props.data;
    const { open } = this.state;
    return (
      <Dialog appBar="Idea" fullScreen open={open} onClose={this.close}>
        {idea && idea.title}
      </Dialog>
    );
  }
}

export const mapDispatchToProps = {
  updateApp: updateApp
};

export const mapStateToProps = (state) => {
  return {
    previousLocation: state.history.navigation.previous
  };
};

export default connect(mapStateToProps, mapDispatchToProps)(
  graphql(ideaQuery, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-first',
        variables: { id: props.id }
      };
    }
  })(DumbIdea)
);