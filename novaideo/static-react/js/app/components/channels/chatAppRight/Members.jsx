/* eslint-disable no-underscore-dangle */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { Translate, I18n } from 'react-redux-i18n';
import { graphql } from 'react-apollo';

import { iconAdapter } from '../../../utils/globalFunctions';
import { channelMembersQuery } from '../../../graphql/queries';
import DetailsSection from './DetailsSection';
import FlatList from '../../common/FlatList';
import UserSmallItem from '../../user/UserSmallItem';

const styles = (theme) => {
  return {
    container: {
      height: '100% !important'
    },
    list: {
      height: '100%',
      backgroundColor: '#fff'
    },
    sectionIcon: {
      marginTop: -3,
      fontSize: '24px !important',
      color: theme.palette.success[500]
    },
    sectionIconActive: {
      '&:hover': {
        color: theme.palette.success[500]
      }
    },
    listItem: {
      borderBottom: '1px solid #e8e8e8'
    },
    listItemActive: {
      borderBottom: 'none'
    }
  };
};

class DumbMembers extends React.Component {
  render() {
    const { data, id, classes, onOpen, open } = this.props;
    const totalCount = data.node && data.node.members && data.node.members.totalCount;
    return (
      <DetailsSection
        id={id}
        classes={{
          sectionIcon: classes.sectionIcon,
          sectionIconActive: classes.sectionIconActive,
          listItem: classes.listItem,
          listItemActive: classes.listItemActive
        }}
        onOpen={onOpen}
        open={open}
        title={
          <span>
            {<Translate value="channels.membersBlockTitle" count={totalCount} />}
          </span>
        }
        Icon={iconAdapter('mdi-set mdi-account-multiple-outline')}
      >
        {open &&
          <FlatList
            data={data}
            getEntities={(entities) => {
              return entities.node && entities.node.members;
            }}
            ListItem={UserSmallItem}
            onEndReachedThreshold={0.5}
            moreBtn={
              <span>
                {I18n.t('common.moreResult')}
              </span>
            }
            className={classes.list}
          />}
      </DetailsSection>
    );
  }
}
export default withStyles(styles, { withTheme: true })(
  graphql(channelMembersQuery, {
    options: (props) => {
      return {
        fetchPolicy: 'cache-and-network',
        notifyOnNetworkStatusChange: true,
        variables: {
          filter: '',
          first: 25,
          after: '',
          id: props.channel.id
        }
      };
    }
  })(DumbMembers)
);