/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { withStyles } from 'material-ui/styles';
import { connect } from 'react-redux';
import { Field, reduxForm, initialize } from 'redux-form';
import SearchIcon from 'material-ui-icons/Search';
import IconButton from 'material-ui/IconButton';
import classNames from 'classnames';

import { iconAdapter } from '../../utils/globalFunctions';
import { renderTextBoxField } from './utils';

const styles = (theme) => {
  return {
    container: {
      backgroundColor: 'white',
      paddingLeft: 20,
      paddingRight: 20,
      flex: 1,
      height: '100%'
    },
    containerAddon: {
      boxShadow: '0 -1px 0 rgba(0,0,0,.1)'
    },
    addon: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between'
    },
    inputContainer: {
      display: 'flex',
      flexDirection: 'row',
      justifyContent: 'space-between',
      outline: 0,
      border: '1px solid #bfbfbf',
      borderRadius: 6,
      resize: 'none',
      color: '#2c2d30',
      fontSize: 16,
      lineHeight: '1.2rem',
      height: '100%',
      alignItems: 'center',
      position: 'relative',
      backgroundColor: 'white',
      flex: 1,
      '& .DraftEditor-root': {
        maxHeight: '100% !important',
        height: 'auto'
      },
      '&:focus-within': {
        border: '1px solid #848484'
      }
    },
    textField: {
      display: 'flex',
      alignItems: 'center',
      position: 'relative',
      height: '100%',
      width: '100%',
      paddingLeft: 10
    },
    placeholder: {
      color: '#000',
      opacity: '.375',
      textOverflow: 'ellipsis',
      overflow: 'hidden',
      whiteSpace: 'nowrap',
      fontStyle: 'normal',
      pointerEvents: 'none',
      position: 'absolute',
      display: 'none',
      top: 0,
      left: 0,
      right: 0,
      maxHeight: '100%'
    },
    placeholderActive: {
      display: 'block',
      top: 8,
      left: 40,
      paddingRight: 40
    },
    submit: {
      color: 'gray',
      opacity: 0.7
    },
    submitActive: {
      opacity: 1,
      color: theme.palette.primary[500],
      cursor: 'pointer'
    },
    action: {
      height: 41,
      width: 35,
      display: 'flex',
      padding: 5
    },
    icon: {
      fontSize: '22px !important',
      color: '#717274',
      marginRight: 5
    }
  };
};

export class DumbSearchForm extends React.Component {
  editor = null;

  getFilters = (query) => {
    return { text: query };
  };

  search = () => {
    const { onSearch } = this.props;
    if (onSearch) onSearch(this.getFilters(this.editor ? this.editor.getPlainText() : ''));
  };

  cancel = () => {
    const { onCancel } = this.props;
    this.initializeForm();
    if (onCancel) onCancel();
  };

  initializeForm = () => {
    const { form } = this.props;
    this.editor.clear();
    this.props.dispatch(
      initialize(form, {
        query: ''
      })
    );
  };

  render() {
    const { classes, title } = this.props;
    const hasQuery = this.editor && this.editor.getPlainText();
    const CancelIcon = iconAdapter('mdi-set mdi-close-circle-outline');
    return (
      <div className={classes.container}>
        <div className={classes.inputContainer}>
          <div className={classNames('inline-editor', classes.textField)}>
            <SearchIcon className={classes.icon} />
            <Field
              props={{
                onEnter: this.search,
                withEmoji: false,
                initRef: (editor) => {
                  this.editor = editor;
                }
              }}
              name="query"
              component={renderTextBoxField}
              type="text"
            />
            <div
              className={classNames(classes.placeholder, {
                [classes.placeholderActive]: !hasQuery
              })}
              aria-hidden="true"
              role="presentation"
              tabIndex="-1"
            >
              {title}
            </div>
          </div>
          {hasQuery &&
            <IconButton onClick={this.cancel}>
              <CancelIcon className={classes.icon} />
            </IconButton>}
        </div>
      </div>
    );
  }
}

// Decorate the form component
const SearchReduxForm = reduxForm({ destroyOnUnmount: false })(DumbSearchForm);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form]
  };
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps)(SearchReduxForm));