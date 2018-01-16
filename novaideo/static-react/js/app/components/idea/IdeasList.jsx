/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';

import IdeaItem from './IdeaItem';
import EntitiesList from '../common/EntitiesList';
import { ideasListQuery } from '../../graphql/queries';
import Divider from './Divider';

export class DumbIdeasList extends React.Component {
  render() {
    const { data } = this.props;
    return (
      <EntitiesList
        listId="ideas"
        isGlobal
        data={data}
        getEntities={(entities) => {
          return entities.ideas;
        }}
        noContentIcon="lightbulb"
        noContentMessage={'noIdeas'}
        noContentFoundMessage={'noIdeaFound'}
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

export default connect(mapStateToProps)(IdeasListGQL);