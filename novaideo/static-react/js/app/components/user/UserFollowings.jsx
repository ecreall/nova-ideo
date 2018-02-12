/* eslint-disable no-undef */
import React from 'react';
import { graphql } from 'react-apollo';
import { withStyles } from 'material-ui/styles';
import StarIcon from 'material-ui-icons/Star';
import { I18n } from 'react-redux-i18n';

import ContentItem from './ContentItem';
import ContentCollapse from './ContentCollapse';
import EntitiesList from '../common/EntitiesList';
import { myFollowingsQuery } from '../../graphql/queries';

const styles = {
  list: {
    height: '100%'
  },
  counter: {
    fontFamily: 'LatoWebLight',
    fontWeight: 100,
    marginLeft: 5,
    fontSize: 14
  }
};

export class DumbUserFollowings extends React.Component {
  render() {
    const { data, classes, onOpen, id, open } = this.props;
    const totalCount = data.account && data.account.followedIdeas.totalCount;
    return (
      <ContentCollapse
        id={id}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            <span>
              {I18n.t('user.myFollowings')}
            </span>
            <span className={classes.counter}>
              {totalCount && `(${totalCount})`}
            </span>
          </span>
        }
        Icon={StarIcon}
      >
        <EntitiesList
          customScrollbar
          data={data}
          getEntities={(entities) => {
            return entities.account && entities.account.followedIdeas;
          }}
          className={classes.list}
          itemHeightEstimation={30}
          progressStyle={{ size: 20, color: 'white' }}
          scrollbarStyle={{ thumbVertical: { backgroundColor: 'rgba(255, 255, 255, 0.22)' } }}
          ListItem={ContentItem}
        />
      </ContentCollapse>
    );
  }
}

export default withStyles(styles)(
  graphql(myFollowingsQuery, {
    options: () => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: { first: 20, after: '' }
      };
    }
  })(DumbUserFollowings)
);