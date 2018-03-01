/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';

import IdeaItem from './IdeaItem';
import FlatList from '../common/FlatList';
import { ideasListQuery } from '../../graphql/queries';
import Divider from './Divider';
import { ACTIONS } from '../../processes';

const styles = {
  list: {
    backgroundColor: 'white',
    border: 'solid 1px #8080802e',
    borderTop: 'none'
  }
};

export class DumbIdeasList extends React.Component {
  render() {
    const { data, classes } = this.props;
    return (
      <FlatList
        scrollEvent="ideas"
        data={data}
        getEntities={(entities) => {
          return entities.ideas;
        }}
        ListItem={IdeaItem}
        Divider={Divider}
        className={classes.list}
      />
    );
  }
}

const IdeasListGQL = graphql(ideasListQuery, {
  options: () => {
    return {
      fetchPolicy: 'cache-and-network',
      notifyOnNetworkStatusChange: true,
      variables: {
        first: 15,
        after: '',
        filter: '',
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      }
    };
  }
})(DumbIdeasList);

export const mapStateToProps = (state) => {
  return {
    filter: state.search.text
  };
};

export default withStyles(styles)(connect(mapStateToProps)(IdeasListGQL));