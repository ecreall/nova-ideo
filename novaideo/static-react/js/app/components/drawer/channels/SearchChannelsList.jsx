/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import FlatList from '../../common/FlatList';
import AllChannels from '../../../graphql/queries/AllChannels.graphql';
import Search from '../../forms/Search';
import SearchChannelItem from './SearchChannelItem';

const styles = {
  container: {
    height: 255,
    '@media  (max-height:450px)': {
      height: 'calc(100vh - 215px)'
    },
    '@media (max-height:370px)': {
      height: 'calc(100vh - 205px)'
    },
    '@media(max-height:280px)': {
      height: 'calc(100vh - 195px)'
    }
  },
  searchContainer: {
    paddingLeft: 0,
    paddingRight: 0,
    borderRadius: 6,
    marginBottom: 15,
    height: 50
  },
  placeholder: {
    top: 16
  }
};

class SearchChannelsList extends React.Component {
  state = {
    filter: { text: '' }
  };

  handelSearch = (filter) => {
    this.setState({ filter: filter });
  };

  handleSearchCancel = () => {
    this.setState({ filter: { text: '' } });
  };

  render() {
    const { classes, onItemClick } = this.props;
    return [
      <Search
        liveSearch
        form="jum-channels-search"
        key="jum-channels-search"
        onSearch={this.handelSearch}
        onCancel={this.handleSearchCancel}
        title={I18n.t('channels.jumpSearch')}
        classes={{
          container: classes.searchContainer,
          placeholder: classes.placeholder
        }}
      />,
      <Query
        notifyOnNetworkStatusChange
        fetchPolicy="cache-and-network"
        query={AllChannels}
        variables={{ first: 25, after: '', filter: this.state.filter.text }}
      >
        {(data) => {
          return (
            <FlatList
              customScrollbar
              className={classes.container}
              data={data}
              getEntities={(entities) => {
                return entities.data ? entities.data.allChannels : entities.allChannels;
              }}
              ListItem={SearchChannelItem}
              itemProps={{ onClick: onItemClick }}
              moreBtn={<span>{I18n.t('common.moreResult')}</span>}
            />
          );
        }}
      </Query>
    ];
  }
}

export default withStyles(styles)(SearchChannelsList);