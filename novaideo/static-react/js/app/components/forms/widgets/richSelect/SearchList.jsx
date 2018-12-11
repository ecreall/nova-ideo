/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import FlatList from '../../../common/FlatList';
import Search from '../../Search';
import SelectItem from './SelectItem';
import { getFormId } from '../../../../utils/globalFunctions';

const styles = {
  container: {
    height: 400,
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

class SearchList extends React.Component {
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
    const {
      id, query, Item, classes, onItemSelect, onItemDeselect, selected, getData
    } = this.props;
    const { filter: { text } } = this.state;
    const formId = getFormId(`${id}select-search`);
    return (
      <React.Fragment>
        <Search
          liveSearch
          form={formId}
          key={formId}
          onSearch={this.handelSearch}
          onCancel={this.handleSearchCancel}
          title={I18n.t('channels.jumpSearch')}
          classes={{
            container: classes.searchContainer,
            placeholder: classes.placeholder
          }}
        />
        <Query
          notifyOnNetworkStatusChange
          fetchPolicy="cache-and-network"
          query={query}
          variables={{ first: 25, after: '', filter: text }}
        >
          {(data) => {
            return (
              <FlatList
                customScrollbar
                className={classes.container}
                data={data}
                getEntities={getData}
                ListItem={SelectItem}
                itemProps={{
                  Item: Item,
                  onSelect: onItemSelect,
                  onDeselect: onItemDeselect,
                  selected: selected
                }}
                moreBtn={<span>{I18n.t('common.moreResult')}</span>}
              />
            );
          }}
        </Query>
      </React.Fragment>
    );
  }
}

export default withStyles(styles)(SearchList);