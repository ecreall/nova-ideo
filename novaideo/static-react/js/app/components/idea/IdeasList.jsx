/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';
import { withStyles } from 'material-ui/styles';

import IdeaItem from './IdeaItem';
import EntitiesList from '../common/EntitiesList';
import { ideasListQuery } from '../../graphql/queries';
import Divider from './Divider';

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
      <EntitiesList
        listId="ideas"
        isGlobal
        className={classes.list}
        data={data}
        getEntities={(entities) => {
          return entities.ideas;
        }}
        itemHeightEstimation={200}
        ListItem={IdeaItem}
        Divider={Divider}
      />
    );
  }
}

const IdeasListGQL = graphql(ideasListQuery, {
  options: (props) => {
    return {
      fetchPolicy: 'cache-and-network',
      notifyOnNetworkStatusChange: true,
      variables: { first: 15, after: '', filter: props.filter }
    };
  }
})(DumbIdeasList);

export const mapStateToProps = (state) => {
  return {
    filter: state.search.text
  };
};

export default withStyles(styles)(connect(mapStateToProps)(IdeasListGQL));