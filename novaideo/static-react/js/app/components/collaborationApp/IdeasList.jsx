/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';

import IdeaItem from '../idea/IdeaItem';
import FlatList from '../common/FlatList';
import IdeasList from '../../graphql/queries/IdeasList.graphql';
import Divider from './Divider';
import { ACTIONS } from '../../processes';

const styles = {
  list: {
    backgroundColor: 'white',
    border: 'solid 1px #8080802e',
    borderTop: 'none'
  }
};

export const DumbIdeasList = ({ classes }) => {
  return (
    <Query
      notifyOnNetworkStatusChange
      fetchPolicy="cache-and-network"
      query={IdeasList}
      variables={{
        first: 15,
        after: '',
        filter: '',
        processIds: [],
        nodeIds: [],
        processTags: [],
        actionTags: [ACTIONS.primary]
      }}
    >
      {(data) => {
        return (
          <FlatList
            scrollEvent="ideas"
            data={data}
            getEntities={(entities) => {
              return entities.data ? entities.data.ideas : entities.ideas;
            }}
            ListItem={IdeaItem}
            Divider={Divider}
            className={classes.list}
          />
        );
      }}
    </Query>
  );
};

export const mapStateToProps = (state) => {
  return {
    filter: state.search.text
  };
};

export default withStyles(styles)(connect(mapStateToProps)(DumbIdeasList));