/* eslint-disable react/no-array-index-key */
import React from 'react';
import { graphql } from 'react-apollo';
import { CircularProgress } from 'material-ui/Progress';
import { withStyles } from 'material-ui/styles';

import { ideaQuery } from '../../graphql/queries';
import Idea from '../idea/IdeaItem';

const styles = {
  progress: {
    width: '100%',
    display: 'flex',
    justifyContent: 'center'
  }
};

export class DumbIdea extends React.Component {
  render() {
    const { data, classes } = this.props;
    if (data.loading) {
      return (
        <div className={classes.progress}>
          <CircularProgress size={30} />
        </div>
      );
    }
    return <Idea node={data.idea} />;
  }
}

export default withStyles(styles)(
  graphql(ideaQuery, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-first',
        variables: { id: props.subject }
      };
    }
  })(DumbIdea)
);