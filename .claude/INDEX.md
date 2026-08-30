# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (149)

```
 10469  GET              /                                                dashboard
 14132  GET              /api/abo/status                                  api_abo_status
 10542  GET              /api/active-recordings                           api_active_recordings
 14203  GET              /api/activity-pulse                              api_activity_pulse
 14010  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20680  GET/POST         /api/audio/config                                api_audio_config
 20710  POST             /api/audio/testtone                              api_audio_testtone
 14076  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14100  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14104  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11996  GET              /api/automation/status                           api_automation_status
 12018  POST             /api/automation/toggle                           api_automation_toggle
 13033  GET              /api/azrael/agents                               api_azrael_agents
 11888  POST             /api/azrael/ask                                  api_azrael_ask
 20878  GET/POST         /api/azrael/context                              api_azrael_context
 12738  GET              /api/azrael/core                                 api_azrael_core
 21029  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21019  GET              /api/azrael/live_status                          api_azrael_live_status
 21037  POST             /api/azrael/live_test                            api_azrael_live_test
 13042  GET              /api/azrael/memories                             api_azrael_memories
 21085  POST             /api/azrael/persona                              api_azrael_persona_set
 21076  GET              /api/azrael/personas                             api_azrael_personas
 21113  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20851  POST             /api/azrael/react                                api_azrael_react
 20887  GET              /api/azrael/reaction                             api_azrael_reaction
 21056  GET              /api/azrael/reactions                            api_azrael_reactions
 21106  GET              /api/azrael/transcript                           api_azrael_transcript
 20991  POST             /api/azrael/tts_test                             api_azrael_tts_test
 20962  GET              /api/azrael/voices                               api_azrael_voices
 21130  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10841  GET              /api/backoff-watch                               api_backoff_watch
 13491  POST             /api/backup/run                                  api_backup_run
 13457  GET              /api/backup/status                               api_backup_status
 13446  POST             /api/backup/system                               api_backup_system
 14042  GET              /api/bandwidth/live                              api_bandwidth_live
 13995  GET              /api/bookmarks                                   api_bookmarks_list
 11104  GET              /api/brain                                       api_brain
 11041  GET              /api/brain/alarms                                api_brain_alarms
 11026  GET              /api/brain/creator                               api_brain_creator
 11003  GET              /api/brain/graph                                 api_brain_graph
 11064  GET              /api/brain/growth                                api_brain_growth
 10019  GET              /api/brain/health                                api_brain_health
 21574  GET              /api/channel/categories                          api_channel_categories
 21580  POST             /api/channel/set                                 api_channel_set
 21427  GET              /api/channels/status                             api_channels_status
 10523  GET              /api/checks                                      api_checks
 20915  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20898  GET              /api/clips                                       api_clips
 20944  POST/DELETE      /api/clips/clear                                 api_clips_clear
 14511  GET              /api/community/stats                             api_community_stats
 22214  GET              /api/data/export                                 api_data_export
 20573  GET              /api/debug/threads                               api_debug_threads
 23061  GET              /api/defense/attacks                             api_defense_attacks
 23028  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23046  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22752  GET              /api/defense/overview                            api_defense_overview
 13553  POST             /api/discord/announce                            api_discord_announce
 13281  GET              /api/discord/clips_week                          api_discord_clips_week
 13497  GET              /api/discord/community                           api_discord_community
 13239  GET              /api/discord/invite                              api_discord_invite
 12839  GET              /api/discord/overview                            api_discord_overview
 12925  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14024  GET              /api/events                                      api_events
 13328  GET              /api/events/stream                               api_events_stream
 14037  GET              /api/forecast/storage                            api_forecast_storage
 12034  GET              /api/freeai/status                               api_freeai_status
 12781  GET              /api/health                                      api_health
 14055  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14051  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20651  GET              /api/highlights                                  api_highlights
 20663  POST             /api/highlights/config                           api_highlights_config
 20759  POST             /api/kickmod/config                              api_kickmod_config
 20804  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20818  GET              /api/kickmod/learned                             api_kickmod_learned
 20845  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20825  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21173  POST             /api/kickmod/say                                 api_kickmod_say
 21149  POST             /api/kickmod/start                               api_kickmod_start
 20730  GET              /api/kickmod/status                              api_kickmod_status
 21160  POST             /api/kickmod/stop                                api_kickmod_stop
 10403  POST             /api/login                                       dashboard_login_submit
 14496  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14465  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13202  GET              /api/notify/status                               api_notify_status
 13213  POST             /api/notify/test                                 api_notify_test
 10627  GET              /api/outcomes                                    api_outcomes
 22051  POST             /api/overlay/config                              api_overlay_config
 22038  POST             /api/overlay/event                               api_overlay_event
 21943  GET              /api/overlay/state                               api_overlay_state
 10660  GET              /api/profile/<username>                          api_profile
 14221  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14063  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14186  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14163  GET              /api/proxy/trend                                 api_proxy_trend
 12489  GET              /api/public/stats                                api_public_stats
 10503  GET              /api/pulse                                       api_pulse
 13631  GET              /api/recording-attempts                          api_recording_attempts
 20375  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20353  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20394  POST             /api/restream/<int:rid>/start                    api_restream_start
 20594  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21905  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20329  POST             /api/restream/create                             api_restream_create
 12614  GET              /api/restream/deck                               api_restream_deck
 11970  GET              /api/restream/health                             api_restream_health
 21927  POST             /api/restream/layout                             api_restream_layout
 20302  GET              /api/restream/list                               api_restream_list
 11939  POST             /api/restream/report                             api_restream_report
 20607  POST             /api/restream/start_all                          api_restream_start_all
 20633  POST             /api/restream/stop_all                           api_restream_stop_all
 12145  GET              /api/restream/testpush                           api_testpush_status
 12170  POST             /api/restream/testpush                           api_testpush_run
 14596  GET              /api/restream/verify                             api_restream_verify
 13259  GET              /api/retention/preview                           api_retention_preview
 13268  POST             /api/retention/run                               api_retention_run
 13980  GET              /api/search                                      api_search
 22799  GET              /api/selftest                                    api_selftest
 20411  GET              /api/shield/stats                                api_shield_stats
 10564  GET              /api/storage                                     api_storage
 10571  POST             /api/storage/cleanup                             api_storage_cleanup
 14117  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11909  GET              /api/stream/timeline                             api_stream_timeline
 12913  GET              /api/stream/transcript                           api_stream_transcript
 10595  GET              /api/summary/preview                             api_summary_preview
 13696  GET              /api/system                                      api_system
 14544  GET              /api/system/check_timing                         api_check_timing
 14659  GET              /api/system/config_drift                         api_config_drift
 12949  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13060  GET              /api/system/preflight                            api_system_preflight
 13186  GET              /api/system/preflight_history                    api_system_preflight_history
 13393  GET              /api/system/resilience                           api_system_resilience
 14015  GET              /api/tags                                        api_tags_list
 10537  GET              /api/top                                         api_top
 10896  GET              /api/trend-7d                                    api_trend_7d
 20976  GET              /api/tts/<fn>                                    api_tts_file
 22079  GET              /api/upload_window                               api_upload_window
 10641  GET              /api/userstats                                   api_userstats
 12537  GET              /api/version                                     api_version
 13669  GET              /archive/<int:eid>/download                      archive_download
 13726  GET              /download/<int:recording_id>                     download
 13609  GET              /health                                          health
 20542  GET              /healthz                                         healthz
 10394  GET              /login                                           dashboard_login_page
 10424  GET              /logout                                          dashboard_logout
 10431  GET              /manifest.webmanifest                            pwa_manifest
 12977  GET              /metrics                                         api_prometheus_metrics
 21888  GET              /overlay                                         overlay_page
 10455  GET              /pwa-icon-<variant>.png                          pwa_icon
 10441  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (210)

```
   176  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   146  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   986  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   726  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   857  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   837  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   875  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   799  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   339  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   350  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   360  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   383  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   390  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   401  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   534  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   632  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1224  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1256  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   323  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   939  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   919  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1092  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1140  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1191  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1050  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   894  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   358  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   622  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   504  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   487  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   479  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   315  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   331  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   666  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   631  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   651  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   538  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    65  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    37  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    33  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    68  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   103  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   265  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   250  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   173  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    51  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    58  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   194  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   221  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   181  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
    61  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
    94  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   102  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    42  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   118  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   148  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   133  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    73  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
    95  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   116  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    63  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   163  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    27  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   182  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   202  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   229  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
    57  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    46  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   204  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    70  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   203  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   225  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    84  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   152  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   130  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    69  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   109  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   159  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
    61  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    86  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
    96  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    35  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    53  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   206  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    83  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    49  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    60  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   125  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   120  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   111  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    36  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    75  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   250  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   317  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   345  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   196  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   263  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   498  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    63  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   161  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   144  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   384  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   815  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   897  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   925  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   936  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   802  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   864  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   851  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   832  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   477  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   472  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   520  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   403  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   730  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   494  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   457  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   430  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   704  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   574  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   663  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   569  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   282  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   747  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   370  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   625  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   780  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   765  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   326  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   564  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   550  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   533  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   590  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   683  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   579  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   306  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   296  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   331  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    48  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    69  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    35  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    85  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   109  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   200  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   195  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   255  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   109  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   256  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    71  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   281  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   213  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   237  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   168  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   133  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   193  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    39  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   219  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   434  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   463  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   383  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   396  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   492  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   369  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   244  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   289  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   313  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   300  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   146  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   258  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   116  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   350  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   405  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   104  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    83  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   115  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
    96  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   106  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    58  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    82  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    36  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   446  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   412  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   471  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   451  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   434  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   427  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
    33  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    73  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   104  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    88  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   114  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   135  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   147  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    72  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
    96  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    50  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   182  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
```

## Discord-Slash-Commands (45)

```
 23525  /ai                     
 23984  /ask                    
 23616  /assign_role            
 23662  /ban                    
 24316  /botstats               
 24240  /clearwarns             
 24280  /clip                   
 24265  /clipoftheweek          
 24107  /clips                  
 23577  /create_category        
 23546  /create_channel         
 23605  /create_group           
 23588  /create_role            
 23562  /create_voice           
 23898  /daily                  
 24014  /event                  
 24057  /events                 
 24153  /follow                 
 24137  /help                   
 23651  /kick                   
 23880  /leaderboard            
 24093  /livenow                
 24123  /post_test              
 23954  /profile                
 23686  /purge                  
 23866  /rank                   
 24080  /recstatus              
 23627  /remove_role            
 23539  /restream_status        
 23638  /set_channel_perms      
 23831  /setup_community        
 23849  /setup_targets          
 24179  /stats                  
 23451  /status                 
 24475  /streaminfo             
 24372  /sys_report             
 24348  /sys_unpause            
 23673  /timeout                
 24251  /topstreamers           
 23481  /track                  
 23465  /tracklist              
 24168  /unfollow               
 23514  /untrack                
 24201  /warn                   
 24225  /warnings               
```

## Discord-Events (4)

```
 24959  on_member_join
 24921  on_message
 24562  on_raw_reaction_add
 24994  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2498-2499   _abo_key
  2519-2537   _abo_probe_dump
 22321-22331  _active_recorder_sync
 17591-17598  _ad_allowlist
 18718-18724  _agent_for
 22333-22351  _ai_calls_total_sync
 18727-18743  _ai_telemetry
 19225-19243  _alert
 25110-25160  _alert_monitor_loop
 25541-25603  _announce_loop
  3440-3443   _anthropic_key
  3450-3452   _anthropic_model
 10147-10150  _arg_int
  2490-2495   _as_dict
 15340-15345  _audio_cfg
 19379-19401  _audio_tap_cmd
 10315-10326  _auth_cookie
 10282-10311  _auth_guard
  1646-1651   _auto_on
 20278-20296  _auto_restream_loop
 26662-26677  _azrael_broadcast_reply
 26562-26584  _azrael_chat_reply
 26545-26559  _azrael_chat_should_reply
 26590-26592  _azrael_gate_cfg
 18748-18762  _azrael_live_state
 21791-21805  _azrael_overlay_state
 19108-19162  _azrael_proactive_loop
 18567-18623  _azrael_reaction_to_chats
 26595-26602  _azrael_reply_all_chats
 26532-26542  _azrael_self_names
 26630-26659  _azrael_send_to
 18765-18786  _azrael_system
 25279-25282  _backup_active
 25360-25373  _backup_loop
 17479-17480  _badwords_path
 25072-25081  _brain_growth_loop
 10972-10999  _brain_growth_snapshot
  2426-2446   _brain_hint_delay
 10964-10966  _brain_history_for
  6531-6559   _brain_notify
 10941-10962  _brain_record
 10968-10970  _brain_stream_recent
 13307-13324  _browser_push
  6575-6662   _build_daily_summary
  2929-3109   _build_native_cmd
 15701-15888  _build_restream_cmd
  3153-3186   _build_ytdlp_cmd
 22273-22280  _cached_probe
  5353-5380   _can_stop_tracking
  1826-1848   _capture_set_cookies
 14280-14283  _cfg_get
 14286-14288  _cfg_set
 21535-21570  _channel_set_all
 14938-14941  _chat_connected
 14944-14960  _chat_disconnected
  8627-8638   _chat_is_forum
 14980-14982  _chat_sanitize
 14984-14993  _chat_src_ok
 14923-14935  _chat_stat
 14963-14966  _chat_stats_snapshot
  3715-3726   _check_ai_alive_sync
  3729-3741   _check_ai_models_sync
 22282-22295  _check_redis_alive_sync
 22297-22317  _check_redis_version_sync
 11571-11614  _classify_pool_anonymity
 11617-11634  _classify_pool_anonymity_bg
   804-808    _claude_chat_sync_metered
 10176-10183  _client_ip
 25635-25662  _clip_prune
 25665-25675  _clip_recfile_for
 26191-26197  _clip_should_velocity
 25716-25798  _clip_to_discord
  3613-3622   _close_ai_session
 26708-26723  _cohost_broadcast
 26693-26694  _cohost_cfg
 26749-26761  _cohost_fire_highlight
 26697-26705  _cohost_gate
 26726-26746  _cohost_highlight
 25847-25881  _community_events_loop
 10795-10797  _conv_messages
  6939-6982   _cookie_alarm_loop
  1898-1902   _cookie_autorefresh_info
  1803-1807   _cookie_header
 13357-13389  _cpu_load_snapshot
  3935-3947   _create_index_safe
 22554-22660  _crowdsec_status
 22500-22551  _crowdsec_via_lapi
 22365-22383  _cscli_bin
 22389-22402  _cscli_path
  6829-6854   _daily_summary_loop
 22420-22437  _darf_journal_lesen
 25084-25107  _db_maintenance_loop
  6798-6826   _db_vacuum_loop
 17614-17638  _detect_foreign_ad
  1384-1395   _diag_path_owner
 19014-19058  _director_finalize
 19825-19832  _director_for
 18963-19011  _director_mark
 26085-26120  _disc_automod_check
 26058-26064  _disc_state_get
 26067-26074  _disc_state_set
 23103-23116  _discord_guild_filesize_bytes
 23302-23311  _discord_invite
 26019-26055  _discord_live_thread
 19165-19177  _discord_notify
 23203-23228  _discord_ops_alert
 25917-26015  _discord_post_user
 23367-25069  _discord_run_once
 23241-23299  _discord_start
 25606-25612  _discord_stop
 23124-23126  _discord_upload_limit_label
 23119-23121  _discord_upload_limit_mb
  6857-6934   _disk_alarm_loop
 28141-28190  _disk_autoclean
 28193-28206  _disk_guard_loop
 28133-28138  _disk_pct
 15297-15299  _drawtext_chain
 13823-13825  _dump_all_threads
 11496-11560  _enrich_proxies_with_geo
  2043-2087   _ensure_cookie_file_netscape
 23314-23364  _ensure_discord_invite
 25812-25844  _ensure_error_channel
  8686-8689   _ensure_notify_topic
 11741-11778  _ensure_proxy_ready
  8640-8667   _ensure_topic
   661-663    _env_int
   666-668    _env_int_range
 25884-25914  _error_channel_loop
 19209-19222  _event_webhook
 14746-14759  _evolution_loop
  5973-6007   _extract_file_payload
  2175-2177   _extract_urls_from_streamurl_node
 22405-22412  _f2b_sudo_hint
 19245-19247  _faster_whisper_available
 17503-17515  _fetch_ldnoobw_de
 11385-11403  _fetch_proxy_list
 19659-19687  _fetch_tiktok_room_id
   737-740    _ff_cmd
 15460-15465  _find_chromium
  3146-3150   _find_external_recorder
  2180-2182   _find_stream_urls
 14331-14356  _fire_webhooks
  7718-7727   _fork_safe
   819-828    _freeai_chat_sync_metered
 22455-22497  _geo_lookup_ips
  3602-3611   _get_ai_session
  7552-7592   _get_live_info
  2716-2723   _get_resolve_semaphore
  7982-8348   _handle_single_tracking
 27959-27961  _hb
 27964-27981  _hb_while
 14998-15000  _highlight_cfg
 15003-15032  _highlight_observe
 15468-15486  _htmlov_screenshot_cmd
 19403-19413  _httpx_proxy
 14364-14376  _in_quiet_hours
 29020-29051  _install_fast_eventloop
 10042-10096  _install_fast_json
 13828-13844  _install_faulthandler
 20450-20459  _intel_ensure_schema
 20497-20532  _intel_index_loop
 20471-20481  _intel_index_one
 20462-20468  _intel_semantic
  5342-5351   _is_authorized
  7883-7889   _is_dead
  2165-2167   _is_hevc
 22440-22446  _is_private_ip
  1548-1555   _is_process_running
  6561-6572   _is_quiet_hours
  1185-1194   _is_upload_window
 10131-10144  _json_error_handler
  6784-6785   _kick_broadcaster_id
 12071-12090  _kick_channel_live
  6696-6738   _kick_follower_count
  6680-6683   _kick_slug
 12564-12595  _kick_user_token
  3984-3987   _kind_from_filename
 14393-14398  _latest_popularity
 17525-17531  _learned_load
 17522-17523  _learned_path
 17533-17541  _learned_save
 20040-20073  _live_react_loop
 19836-20029  _live_react_worker
 18626-18637  _live_transcript_push
 20031-20038  _live_users
 19061-19105  _living_title_loop
 17482-17490  _load_banned_words_file
  1724-1797   _load_cookies_dict
 25285-25357  _local_backup_scan
 10113-10127  _log_5xx
 15896-15908  _looks_like_codec_err
 15891-15893  _looks_like_source_expired
  7799-7829   _loop_fehler
 13848-13857  _loop_heartbeat
 27929-27956  _loop_lag_monitor
 13860-13928  _loop_watchdog_thread
 18506-18520  _loyalty_add
 18497-18503  _loyalty_get
 18523-18531  _loyalty_top
 14530-14532  _manual_donations_total
  7891-7892   _mark_dead
 12242-12258  _marketing_loop
 26609-26627  _maybe_handle_command
 28292-28316  _maybe_hype_clip
  3902-3925   _migrate_columns
 26888-26899  _mod_is_exempt
 26902-26907  _mod_warn_first
 26910-26913  _mod_warn_text
 14786-14794  _modlog
   938-940    _multistream_targets
  7730-7731   _nc_create_subprocess_exec
  7734-7735   _nc_create_subprocess_shell
 12494-12511  _news_loop
 14824-14826  _normalize_ingest
  2357-2374   _note_check_duration
  8680-8683   _notify_topic_name
 18652-18660  _oracle_memories
 18918-18952  _oracle_memorize
 18663-18676  _oracle_persona
 18645-18649  _oracle_recent_text
 15123-15131  _ov_atomic_write
 15111-15117  _ov_bar
 17438-17450  _ov_clip_text
 15120-15121  _ov_oneline
 21855-21884  _overlay_push
 15414-15457  _overlay_render_size
 14885-14889  _overlay_session_reset
 21807-21810  _overlay_src_ok
 17601-17611  _own_invites
 15409-15411  _parse_size
 22668-22748  _parse_ssh_attacks
  7154-7187   _pause_resume_cmd
  1852-1896   _persist_refreshed_cookies
  1690-1722   _pick_checked_pull_proxy
 10212-10225  _pin_auth_value
 10271-10272  _pin_clear_fail
 10251-10254  _pin_locked
 10257-10268  _pin_note_fail
 10228-10248  _pin_ok
 21697-21699  _piper_available
 21662-21684  _piper_list_voices
 21704-21729  _piper_pick_model
 21741-21788  _piper_say
 21655-21659  _piper_voice_roots
 14293-14328  _post_json_threaded
 15388-15406  _probe_video_size
  1576-1593   _proc_is_recorder
 11483-11494  _proxy_geo_cache_put
 11710-11738  _proxy_pool_refresh_loop
  1656-1687   _proxy_report_recording
 13813-13815  _prune_stall_dumps
 12312-12433  _public_stats
 19180-19206  _push_notify
 10373-10375  _pwa_dir
 11454-11469  _quick_validate_proxy
 14359-14361  _quiet_hours_config
 10338-10371  _rate_guard
 18471-18477  _react_warn
  7638-7677   _reap_proc
  2397-2419   _record_check_outcome
   732-734    _redact_stream_urls
 11637-11707  _refresh_proxy_pool
 21687-21693  _resolve_piper_model
  2191-2281   _resolve_via_html
  2539-2693   _resolve_via_webcast_api_v2
  2756-2818   _resolve_via_ytdlp
 26236-26365  _resolve_youtube_ingest
 20112-20119  _restream_active_platforms
 14870-14881  _restream_active_sources
 19690-19789  _restream_chat_guardian
 15035-15107  _restream_chat_push
 14797-14809  _restream_enabled
 15489-15576  _restream_html_overlay_start
 15579-15592  _restream_html_overlay_stop
  1133-1135   _restream_layout_mode
 14835-14858  _restream_overlay_files
 20077-20109  _restream_platform_state
 20240-20275  _restream_resume_after_restart
 15640-15698  _restream_tts_enqueue_wav
 15350-15382  _restream_tts_feeder
 15347-15348  _restream_tts_fifo_path
 15595-15622  _restream_tts_start
 15624-15638  _restream_tts_stop
 20122-20237  _restream_verify_loop
 25250-25262  _retention_loop
 25209-25247  _retention_scan
  2501-2503   _room_is_abo
  6011-6128   _run_ai_call
 13951-13964  _run_async_from_flask
 22449-22452  _run_priv
 29008-29016  _run_selfcheck_and_exit
 25265-25276  _s3_client
  7918-7969   _safe_send
  4606-4622   _sample_net_throughput
 17492-17500  _save_banned_words_file
  2449-2476   _schedule_next_check
 25163-25206  _scheduler_loop
  3928-3932   _schema_pk
 13968-13973  _scraper_session
 26916-26955  _screen_full
 12797-12834  _sec_headers
  2170-2172   _select_stream_from_data_section
 28821-29005  _selfcheck
  8692-8726   _send_live_notice
  1208-1212   _should_defer_upload
 25678-25713  _shrink_for_discord
 10378-10390  _sicheres_ziel
 28213-28230  _sign_health_check
 28233-28252  _sign_health_loop
  7747-7758   _spawn
  7761-7791   _spawn_from_flask
 22792-22795  _st_befund
 19415-19656  _start_chat_listener
 13931-13948  _start_loop_watchdog
 12457-12485  _stats_loop
 12436-12439  _stats_output_path
 12442-12454  _stats_write
  8420-8436   _storage_cleanup_loop
 28272-28279  _story_for
  3208-3214   _stream_url_expiry
  3223-3229   _stream_url_is_fresh
  3216-3221   _stream_url_ttl
 17565-17572  _streamer_persona_get
 17547-17553  _streamer_personas_load
 17544-17545  _streamer_personas_path
 17555-17563  _streamer_personas_save
 15302-15306  _studio_chain
 25382-25504  _system_backup
 25507-25537  _system_backup_loop
 11406-11445  _test_proxy
 12112-12121  _testpush_cfg
 12124-12141  _testpush_exec
 12093-12109  _testpush_resolve_live
  7894-7915   _tg_sprache_setzen
  8599-8609   _tg_topics_load_into_mem
  8596-8597   _tg_topics_path
  8611-8618   _tg_topics_save
 10186-10194  _token_ok
  8621-8625   _topic_forget
 14379-14390  _tracking_max_duration
  4193-4207   _tracking_remove_cleanup
  4224-4236   _tracking_resume_cleanup
  1442-1465   _try_attach_file_handler
 21731-21739  _tts_cleanup
 12049-12053  _tunnel_effective
 21194-21247  _twitch_channel_status
 26958-27101  _twitch_chat_loop
 26772-26875  _twitch_eventsub_loop
  1231-1244   _upload_queue_add
  1255-1257   _upload_queue_count
  1214-1223   _upload_queue_load
  1204-1206   _upload_queue_path
  1246-1253   _upload_queue_remove
  1225-1229   _upload_queue_save
  1259-1300   _upload_window_loop
  7611-7618   _uptime_s
 14812-14821  _url_host
   712-729    _url_ohne_zugang
   797-801    _usage_record_claude
  7832-7876   _verbindung_verloren
  6741-6772   _viewer_sample_loop
  6788-6795   _viewer_stats
 10275-10278  _wants_html
  7621-7635   _warn_empty_env
 28002-28123  _watchdog_loop
 26511-26519  _wchat_thank_ok
 19249-19279  _whisper_get_model
  7708-7715   _whisper_native_section
 18458-18464  _whisper_pool
 19348-19377  _whisper_segments
 19281-19345  _whisper_transcribe
 15133-15295  _write_restream_overlay
 27129-27208  _youtube_api_chat_loop
 21250-21353  _youtube_api_status
 21356-21423  _youtube_channel_status
 27211-27371  _youtube_chat_loop
 26371-26384  _youtube_restream_autoconfig
 26387-26411  _youtube_restream_autoconfig_inner
 26478-26506  _youtube_send
 21491-21532  _youtube_set_channel
 26414-26448  _yt_access_token
 26451-26466  _yt_live_chat_id
 27122-27126  _yt_oauth_configured
 26474-26475  _yt_sendrate_cfg
 27104-27119  _yt_timeout
  2740-2741   _ytdlp_detect_available
  2743-2754   _ytdlp_note_result
 13818-13820  _zombie_child_count
  7488-7512   about
  4103-4107   add_ai_log_entry
  4020-4023   add_archive_entry
  4719-4734   add_archive_rule
  4395-4429   add_recording
  4168-4185   add_tracking
  6131-6164   ai
  3755-3806   ai_chat
  3840-3850   ai_history_append
  3852-3857   ai_history_clear
  3829-3838   ai_history_load
  3814-3827   ai_rate_limit_check
  6193-6201   aireset
 18789-18808  azrael_chat
 27376-27498  brain_cmd
  3232-3416   build_recording_cmd
  4188-4191   bulk_add_trackings
  6985-7044   bulkadd
  8439-8579   check_all_trackings
  4240-4252   claim_live_transition
 17641-18396  class KickModerator
 15911-17325  class RestreamManager
 11823-11865  classify_proxy_anonymity
  6239-6437   cleanup
  5202-5243   cleanup_old_recordings
  4386-4393   clear_recording
 26123-26188  clip_moment
  4550-4599   compute_storage_forecast
  7107-7151   cookies_cmd
  4159-4165   count_trackings_for_chat
  4090-4101   decide_preferred_recorder
  4030-4033   delete_archive_entry
  4736-4744   delete_archive_rule
  5668-5815   diag
 27610-27671  einnahmen_cmd
  4544-4547   find_recordings_by_fingerprint
  4051-4067   finish_recording_attempt
  4212-4214   get_all_active_trackings
  4118-4121   get_all_checks
  4431-4434   get_all_recordings
  4493-4495   get_all_tags_with_counts
  4521-4524   get_annotations_for_recording
  4025-4028   get_archive_entry
  4514-4517   get_bookmarked_recordings
  1919-2036   get_cookie_health
  4481-4487   get_event_log
  4074-4088   get_last_recording_attempt
  2821-2926   get_live_status
  5002-5005   get_manual_recordings
  4529-4532   get_or_compute_inspect_sync
  5278-5322   get_outcome_breakdown
  4500-4503   get_priority_poll_interval
  4697-4706   get_profile_snapshots
  4069-4072   get_recent_recording_attempts
  4436-4439   get_recording_by_id
  4507-4510   get_recording_note
  3550-3573   get_redis
  4148-4151   get_stats
  5169-5200   get_storage_stats
  4837-4839   get_tiktok_status_distribution
  4254-4263   get_tracking_state
  4209-4210   get_trackings_for_group
  5018-5021   get_trash_recordings
  9347-10010  handle_recording_finished
  3950-3975   init_db
  5092-5146   inspect_stream_url
 21850-21852  is_revenue_platform
  4709-4717   list_archive_rules
  5472-5510   live
  7972-7980   live_check_worker
  3625-3659   llm_chat
  3682-3710   llm_chat_sync
  3667-3679   llm_list_models
  4447-4473   log_event
  1510-1543   log_recording_failure
  7301-7350   logs_cmd
 28320-28811  main
  6167-6190   on_ai_media
  7427-7453   on_ai_reply
  7456-7485   on_azrael_mention
  7517-7547   on_callback
 18811-18915  oracle_handle
  7190-7193   pause_tracking
  5332-5337   profile_keyboard
  7252-7298   quota
  8350-8417   reaper_loop
  4833-4835   record_tiktok_status
  6206-6236   recstatus
  3575-3583   redis_get_json
  3585-3591   redis_set_json
 27674-27684  report_cmd
 11868-11870  report_proxy_result
  2284-2311   resolve_tiktok_live_stream
  5013-5016   restore_recording
  7196-7199   resume_tracking
  4747-4827   run_archive_rules
 27687-27909  run_bot
 13740-13787  run_flask
  4625-4670   sample_bandwidth_for_active
  4676-4695   save_profile_snapshot
  4110-4116   save_tiktok_check
  4378-4384   set_recording_file
  4217-4221   set_tracking_paused
  5008-5011   soft_delete_recording
  8732-9345   split_and_send_video
  5385-5427   start
  4035-4049   start_recording_attempt
  6440-6478   stats
  4983-5000   stop_manual_recording
  7202-7249   stoprec
  6665-6673   summary_cmd
  7353-7424   sysres
  5817-5961   teststream
  5429-5470   tiktok
  7047-7104   topusers
  5547-5604   track
  5512-5544   track_exact
  5618-5666   tracklist
  4849-4981   trigger_manual_recording
  4339-4376   try_acquire_recording_lock
  5024-5083   universal_search
  5606-5616   untrack
 27501-27607  update_cmd
  4539-4542   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
binresolve.py          resolve
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, live_ping, note_chatter, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
director.py            class LiveDirector, configure
discordlimits.py       describe, effective_upload_mb, gate_mb, guild_limit_mb
donations.py           configure, fmt_eur, parse_number, source_allowed, to_eur, unknown_count
donationsdb.py         manual_rows, manual_total, parse_eur
envnum.py              clamp_float, clamp_int, env_float, env_int, env_int_range
eventquery.py          build_query
evolution.py           analyze, build_dir, conf, configure, cycle, engineering_note, next_version, write_build
ffbuild.py             ff_cmd
ffdiag.py              clip_caption_escape, ffprobe_duration, redact_cmd_for_log
ffmpeg_filters.py      drawtext_chain, studio_chain
ffver.py               parse_version
filepayload.py         classify_downloaded, size_reject
flapguard.py           class FlapConfig, class FlapUrteil, class FlapWatch
fmt.py                 fmt_duration, fmt_size_mb, pre_table, utc_clock
freeai.py              alive_sync, bases_status, chat, chat_stream, chat_sync, configure, diagnose, last_errors, list_models_sync
highlights.py          check, new_state, observe, score
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        resolve_model_path, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restrend.py            rising_trend
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
youtube_api.py         active_broadcast_params, ban_payload, is_self, list_params, merge_video_snippet, parse_broadcast_id, parse_error, parse_messages, parse_video_snippet, video_list_params, video_update_body
ytoauth.py             access_token, authorize_url, configure, exchange_code, forget, invalidate_access, revoke, set_channel, status
```

## brain/ — öffentliche Symbole

```
__init__.py            class Brain, get_brain
agents.py              class Agent, class AgentManager, class AnalyticsAgent, class DiskAgent, class HealthAgent, class LearningAgent, class ProxyHealthAgent, class RecordingAgent, class RecoveryAgent, class RestreamSentinelAgent, class ScoutAgent, class SentinelAgent, class SwapAgent, class ToxicityAgent, class UptimeAgent
knowledge.py           class KnowledgeGraph
llm.py                 class BudgetExhausted, class LLMRuntime
memory.py              class Memory
report.py              weekly
router.py              class Task, class TaskRouter, class Unhandled
rules.py               class Rule, class RulesEngine
scheduler.py           class Scheduler
semantic.py            class SemanticMemory
state.py               class Entity, class StateMachine
test_bughunt.py        db_conn, main
test_m1.py             main
test_m3.py             main
test_m4.py             main
test_m5.py             main
test_m6.py             class LlamaCppMock, main
test_m7.py             db_conn, main
```
