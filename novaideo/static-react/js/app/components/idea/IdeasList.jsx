/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { connect } from 'react-redux';

import IdeaItem from './IdeaItem';
import EntitiesList from '../common/EntitiesList';
import { ideasListQuery } from '../../graphql/queries';

export class DumbIdeasList extends React.Component {
  render() {
    const { data } = this.props;

    return (
      <EntitiesList
        data={data}
        getEntities={(entities) => {
          return entities.ideas;
        }}
        noContentIcon="lightbulb"
        noContentMessage={'noIdeas'}
        noContentFoundMessage={'noIdeaFound'}
        offlineFilter={(entity, text) => {
          return (
            entity.node.title.toLowerCase().search(text) >= 0 ||
            entity.node.text.toLowerCase().search(text) >= 0 ||
            entity.node.keywords.join(' ').toLowerCase().search(text) >= 0
          );
        }}
        ListItem={IdeaItem}
      />
    );
  }
}

const IdeasListGQL = graphql(ideasListQuery, {
  options: (props) => {
    return {
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