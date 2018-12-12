/* eslint-disable no-undef */
import React from 'react';
import { Query } from 'react-apollo';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';

import FlatList from '../../../common/FlatList';
import Search from '../../Search';
import SelectItem from './SelectItem';
import { getFormId } from '../../../../utils/globalFunctions';
import Button from '../../../styledComponents/Button';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  container: {
    height: 200,
    '@media  (max-height:450px)': {
      height: 'calc(100vh - 215px)'
    },
    '@media (max-height:200px)': {
      height: 'calc(100vh - 205px)'
    },
    '@media(max-height:150px)': {
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
  },
  footer: {
    padding: 15,
    display: 'flex',
    justifyContent: 'center'
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
      id, query, Item, classes, theme, onItemSelect, onItemDeselect, selected, getData, onValidate
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
              <React.Fragment>
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
                <div className={classes.footer}>
                  <Button
                    onClick={onValidate}
                    background={theme.palette.success[800]}
                    className={classes.button}
                    disabled={!selected || selected.length === 0}
                  >
                    {I18n.t('forms.richSelect.validateList')}
                  </Button>
                </div>
              </React.Fragment>
            );
          }}
        </Query>
      </React.Fragment>
    );
  }
}

export default withStyles(styles, { withTheme: true })(SearchList);