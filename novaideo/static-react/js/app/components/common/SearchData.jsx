/* eslint-disable react/no-array-index-key */
import React from 'react';
import { withStyles } from '@material-ui/core/styles';
import { connect } from 'react-redux';
import { Translate } from 'react-redux-i18n';
// import IconButton from '@material-ui/core/IconButton';

// import { iconAdapter } from '../../utils/globalFunctions';
import { search } from '../../actions/collaborationAppActions';

const styles = (theme) => {
  return {
    container: {
      background: theme.palette.info[500],
      color: 'white',
      padding: 16,
      margin: 0,
      fontSize: 16,
      marginBottom: 20,
      borderRadius: 6,
      boxShadow: 'rgba(128, 128, 128, 0.4) 0px 0px 1px 1px'
    },
    searchText: {
      fontWeight: 900,
      fontSize: 30,
      textShadow: 'rgba(0, 0, 0, 0.4) 0px 1px 1px'
    }
  };
};

class SearchData extends React.Component {
  handleSearchCancel = () => {
    const { id } = this.props;
    this.props.search(id, '');
  };

  render() {
    const { filter, count, classes } = this.props;
    // const CancelIcon = iconAdapter('mdi-set mdi-close-circle-outline');
    return (
      <div className={classes.container}>
        {/* <IconButton onClick={this.handleSearchCancel}>
          <CancelIcon className={classes.icon} />
        </IconButton> */}
        <span className={classes.searchText}>{count}</span> <Translate value="common.searchData" count={count || 0} />
        <span className={classes.searchText}>{filter && filter.text}</span>
      </div>
    );
  }
}

export const mapDispatchToProps = {
  search: search
};

const mapStateToProps = (state, props) => {
  return {
    filter: state.search[props.id]
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(SearchData));