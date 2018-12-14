/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Form as ReduxForm, Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import IconButton from '@material-ui/core/IconButton';
import Icon from '@material-ui/core/Icon';
import Tooltip from '@material-ui/core/Tooltip';

import { renderSelect } from '../forms/utils';
import { OPINIONS } from '../../constants';
import { openFilter } from '../../actions/collaborationAppActions';

const styles = {
  button: {
    marginLeft: '5px !important'
  },
  container: {
    padding: '20px 25px',
    width: '100%',
    fontSize: 17,
    lineHeight: 1.5
  },
  title: {
    marginLeft: 5
  },
  circle: {
    color: 'gray',
    fontSize: 22
  },
  unfavorable: {
    color: '#f13b2d',
    textShadow: '0 0px 4px #f13b2d'
  },
  to_study: {
    color: '#ef6e18',
    textShadow: '0 0px 4px #ef6e18'
  },
  favorable: {
    color: '#4eaf4e',
    textShadow: '0 0px 4px #4eaf4e'
  }
};

export class DumIdeasFilter extends React.Component {
  componentDidUpdate() {
    const {
      id, live, formData, openFilterSection
    } = this.props;
    if (live && formData.values) {
      openFilterSection(id, { states: Object.keys(formData.values.examination) });
    }
  }

  renderOpinion = (key, value) => {
    const { classes } = this.props;
    return (
      <div>
        <Icon className={classNames(classes.circle, classes[key], 'mdi-set mdi-checkbox-blank-circle')} />
        <span className={classes.title}>{I18n.t(value)}</span>
      </div>
    );
  };

  render() {
    const { adapters, classes } = this.props;

    const opinionsBase = adapters.opinions || OPINIONS;
    const opinions = {};
    Object.keys(opinionsBase).forEach((key) => {
      opinions[key] = this.renderOpinion(key, opinionsBase[key]);
    });

    return (
      <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
        <Field
          props={{
            label: (
              <Tooltip title={I18n.t('forms.idea.keywords')} placement="top">
                <IconButton className={classes.button}>
                  <Icon className="mdi-set mdi-tag-multiple" />
                </IconButton>
              </Tooltip>
            ),
            options: opinions,
            inline: true,
            initRef: (keywordsPicker) => {
              this.keywordsPicker = keywordsPicker;
            }
          }}
          withRef
          name="examination"
          component={renderSelect}
        />
      </ReduxForm>
    );
  }
}

// Decorate the form component
const DumIdeasFilterReduxForm = reduxForm({
  destroyOnUnmount: false,
  touchOnChange: true
})(DumIdeasFilter);

const mapStateToProps = (state, props) => {
  return {
    formData: state.form[props.form],
    adapters: state.adapters
  };
};

export const mapDispatchToProps = {
  openFilterSection: openFilter
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(DumIdeasFilterReduxForm));