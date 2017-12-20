/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';

import { ideaQuery } from '../../graphql/queries';

export class DumbIdea extends React.Component {
  render() {
    const { idea } = this.props.data;
    return (
      <div>
        {idea.title}
      </div>
    );
  }
}

export default graphql(ideaQuery, {
  options: (props) => {
    return {
      fetchPolicy: 'cache-first',
      variables: { id: props.navigation.state.params.ideaId }
    };
  }
})(DumbIdea);