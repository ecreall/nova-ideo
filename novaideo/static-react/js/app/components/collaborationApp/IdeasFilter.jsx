/* eslint-disable react/no-array-index-key, no-confusing-arrow */
import React from 'react';
import { Form as ReduxForm, Field, reduxForm } from 'redux-form';
import { connect } from 'react-redux';
import classNames from 'classnames';
import { withStyles } from '@material-ui/core/styles';
import { I18n } from 'react-redux-i18n';
import Icon from '@material-ui/core/Icon';
import Grid from '@material-ui/core/Grid';
import Moment from 'moment';

import { renderDatePicker, renderSelect, renderRichSelect } from '../forms/utils';
import { OPINIONS } from '../../constants';
import { openFilter } from '../../actions/collaborationAppActions';
import Members from '../../graphql/queries/Members.graphql';
import MemberItem from '../forms/processes/ideaProcess/MemberItem';
import { getIdeaStates } from '../../utils/processes';
import { STATE_LABEL } from '../../processes';

const styles = {
  root: {
    width: '100%'
  },
  form: {
    paddingTop: 10
  },
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
  },
  itemText: {
    fontSize: 13
  },
  section: {
    marginBottom: 24,
    fontSize: 15
  },
  sectionTitleContainer: {
    position: 'relative',
    marginBottom: 10,
    '&::before': {
      display: 'block',
      content: '""',
      position: 'absolute',
      top: '50%',
      left: 0,
      right: 0,
      height: 0,
      borderBottom: '1px solid #e8e8e8'
    }
  },
  sectionTitle: {
    position: 'relative',
    display: 'inline-block',
    padding: '0 8px 0 0',
    margin: 0,
    fontWeight: 'inherit',
    lineHeight: 'inherit',
    fontSize: 13,
    color: '#717274',
    backgroundColor: '#f3f3f3'
  },
  sectionContent: {},
  listPadding: {
    padding: 0
  },
  textInput: {
    height: 25,
    width: '100%',
    padding: 4
  },
  textInputLabel: {
    fontSize: 13
  },
  formTitle: {
    paddingTop: 10,
    marginBottom: 0,
    fontSize: 15,
    fontWeight: 700,
    color: '#717274'
  }
};

export class DumIdeasFilter extends React.Component {
  componentDidUpdate() {
    const {
      id, filterOpened, formData, openFilterSection
    } = this.props;
    if (filterOpened && formData && formData.values) {
      const {
        examination, authors, states, startDate, endDate
      } = formData.values;
      openFilterSection(id, {
        startDate: startDate,
        endDate: endDate,
        states: states ? Object.keys(states) : [],
        examination: examination ? Object.keys(examination) : [],
        authors: authors
          ? authors.map((author) => {
            return author.oid;
          })
          : []
      });
    }
  }

  renderOpinion = (key, value) => {
    const { classes } = this.props;
    return (
      <div className={classes.itemText}>
        <Icon className={classNames(classes.circle, classes[key], 'mdi-set mdi-checkbox-blank-circle')} />
        <span className={classes.title}>{I18n.t(value)}</span>
      </div>
    );
  };

  getOpinions = () => {
    const { adapters } = this.props;
    const opinionsBase = adapters.opinions || OPINIONS;
    const opinions = {};
    Object.keys(opinionsBase).forEach((key) => {
      opinions[key] = this.renderOpinion(key, opinionsBase[key]);
    });
    return opinions;
  };

  renderState = (value) => {
    const { classes } = this.props;
    const state = STATE_LABEL.idea[value];
    const StateIcon = state.icon;
    const stateTitle = state.title;
    return (
      <div className={classes.itemText}>
        <StateIcon />
        <span className={classes.title}>{I18n.t(stateTitle)}</span>
      </div>
    );
  };

  getStates = () => {
    const { config, isLogged } = this.props;
    const ideaState = getIdeaStates(config);
    delete ideaState.toStudy;
    delete ideaState.favorable;
    delete ideaState.unfavorable;
    if (!isLogged) {
      delete ideaState.published;
      delete ideaState.private;
      delete ideaState.archived;
    }
    const states = {};
    Object.keys(ideaState).forEach((key) => {
      const value = ideaState[key];
      states[value] = this.renderState(value);
    });
    return states;
  };

  hasSection = (section) => {
    const { sections } = this.props;
    return !sections || (sections && sections.includes(section));
  };

  render() {
    const {
      id, config, formData, classes
    } = this.props;
    const now = Moment();
    const data = formData || {};
    const { values } = data;
    const startDate = (values && values.startDate && Moment(values.startDate)) || null;
    const endDate = (values && values.endDate && Moment(values.endDate)) || null;
    return (
      <div className={classes.root}>
        <div className={classes.formTitle}>{I18n.t('forms.filter.filterBy')}</div>
        <ReduxForm className={classes.form} onSubmit={this.handleSubmit}>
          <Grid container spacing={24}>
            {this.hasSection('states') ? (
              <Grid item xs={3}>
                <div className={classes.section}>
                  <div className={classes.sectionTitleContainer}>
                    <div className={classes.sectionTitle}>{I18n.t('forms.filter.states')}</div>
                  </div>
                  <div className={classes.sectionContent}>
                    <Field
                      props={{
                        options: this.getStates(),
                        inline: true,
                        fontSize: 'small',
                        classes: { padding: classes.listPadding }
                      }}
                      name="states"
                      component={renderSelect}
                    />
                  </div>
                </div>
              </Grid>
            ) : null}
            {this.hasSection('examination') && config.examineIdeas ? (
              <Grid item xs={3}>
                <div className={classes.section}>
                  <div className={classes.sectionTitleContainer}>
                    <div className={classes.sectionTitle}>{I18n.t('forms.filter.examination')}</div>
                  </div>
                  <div className={classes.sectionContent}>
                    <Field
                      props={{
                        options: this.getOpinions(),
                        inline: true,
                        fontSize: 'small',
                        classes: { padding: classes.listPadding }
                      }}
                      name="examination"
                      component={renderSelect}
                    />
                  </div>
                </div>
              </Grid>
            ) : null}
            {this.hasSection('authors') ? (
              <Grid item xs={3}>
                <div className={classes.section}>
                  <div className={classes.sectionTitleContainer}>
                    <div className={classes.sectionTitle}>{I18n.t('forms.filter.authors')}</div>
                  </div>
                  <div className={classes.sectionContent}>
                    <Field
                      props={{
                        query: Members,
                        Item: MemberItem,
                        id: id,
                        placeholder: I18n.t('forms.filter.addMembers'),
                        getData: (entities) => {
                          return entities.data ? entities.data.members : entities.members;
                        }
                      }}
                      name="authors"
                      component={renderRichSelect}
                    />
                  </div>
                </div>
              </Grid>
            ) : null}
            {this.hasSection('date') ? (
              <Grid item xs={3}>
                <div className={classes.section}>
                  <div className={classes.sectionTitleContainer}>
                    <div className={classes.sectionTitle}>{I18n.t('forms.filter.date')}</div>
                  </div>
                  <div className={classes.sectionContent}>
                    <Field
                      props={{
                        type: 'date',
                        placeholder: I18n.t('forms.filter.startDate'),
                        selectsStart: true,
                        maxDate: endDate || now,
                        startDate: startDate,
                        endDate: endDate,
                        isClearable: true,
                        classes: {
                          root: classes.textInput,
                          label: classes.textInputLabel
                        }
                      }}
                      name="startDate"
                      component={renderDatePicker}
                    />
                    <Field
                      props={{
                        type: 'date',
                        placeholder: I18n.t('forms.filter.endDate'),
                        selectsEnd: true,
                        maxDate: now,
                        minDate: startDate,
                        startDate: startDate,
                        endDate: endDate,
                        isClearable: true,
                        classes: {
                          root: classes.textInput,
                          label: classes.textInputLabel
                        }
                      }}
                      name="endDate"
                      component={renderDatePicker}
                    />
                  </div>
                </div>
              </Grid>
            ) : null}
          </Grid>
        </ReduxForm>
      </div>
    );
  }
}

// Decorate the form component
const DumIdeasFilterReduxForm = reduxForm({
  destroyOnUnmount: false,
  touchOnChange: true
})(DumIdeasFilter);

const mapStateToProps = (state, { form, id }) => {
  return {
    config: state.globalProps.site,
    formData: state.form[form],
    adapters: state.adapters,
    filterOpened: !!state.filter[id],
    isLogged: state.network.isLogged
  };
};

export const mapDispatchToProps = {
  openFilterSection: openFilter
};

export default withStyles(styles, { withTheme: true })(connect(mapStateToProps, mapDispatchToProps)(DumIdeasFilterReduxForm));