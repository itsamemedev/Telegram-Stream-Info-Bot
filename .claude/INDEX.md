# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (153)

```
 10455  GET              /                                                dashboard
 14144  GET              /api/abo/status                                  api_abo_status
 10528  GET              /api/active-recordings                           api_active_recordings
 14215  GET              /api/activity-pulse                              api_activity_pulse
 14022  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20780  GET/POST         /api/audio/config                                api_audio_config
 20810  POST             /api/audio/testtone                              api_audio_testtone
 14088  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14112  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14116  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11982  GET              /api/automation/status                           api_automation_status
 12004  POST             /api/automation/toggle                           api_automation_toggle
 13019  GET              /api/azrael/agents                               api_azrael_agents
 11874  POST             /api/azrael/ask                                  api_azrael_ask
 20978  GET/POST         /api/azrael/context                              api_azrael_context
 12724  GET              /api/azrael/core                                 api_azrael_core
 21130  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21120  GET              /api/azrael/live_status                          api_azrael_live_status
 21138  POST             /api/azrael/live_test                            api_azrael_live_test
 13028  GET              /api/azrael/memories                             api_azrael_memories
 21186  POST             /api/azrael/persona                              api_azrael_persona_set
 21177  GET              /api/azrael/personas                             api_azrael_personas
 21214  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20951  POST             /api/azrael/react                                api_azrael_react
 20987  GET              /api/azrael/reaction                             api_azrael_reaction
 21157  GET              /api/azrael/reactions                            api_azrael_reactions
 21207  GET              /api/azrael/transcript                           api_azrael_transcript
 21092  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21061  GET              /api/azrael/voices                               api_azrael_voices
 21231  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10827  GET              /api/backoff-watch                               api_backoff_watch
 13503  POST             /api/backup/run                                  api_backup_run
 13469  GET              /api/backup/status                               api_backup_status
 13458  POST             /api/backup/system                               api_backup_system
 14054  GET              /api/bandwidth/live                              api_bandwidth_live
 14007  GET              /api/bookmarks                                   api_bookmarks_list
 11090  GET              /api/brain                                       api_brain
 11027  GET              /api/brain/alarms                                api_brain_alarms
 11012  GET              /api/brain/creator                               api_brain_creator
 10989  GET              /api/brain/graph                                 api_brain_graph
 11050  GET              /api/brain/growth                                api_brain_growth
 10005  GET              /api/brain/health                                api_brain_health
 21675  GET              /api/channel/categories                          api_channel_categories
 21681  POST             /api/channel/set                                 api_channel_set
 21528  GET              /api/channels/status                             api_channels_status
 20424  POST             /api/chat/send                                   api_chat_send
 13223  GET              /api/chat/send_status                            api_chat_send_status
 10509  GET              /api/checks                                      api_checks
 21015  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20998  GET              /api/clips                                       api_clips
 21043  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20702  GET              /api/cohost                                      api_cohost
 20714  POST             /api/cohost/config                               api_cohost_config
 14523  GET              /api/community/stats                             api_community_stats
 22315  GET              /api/data/export                                 api_data_export
 20628  GET              /api/debug/threads                               api_debug_threads
 23142  GET              /api/defense/attacks                             api_defense_attacks
 23109  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23127  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22833  GET              /api/defense/overview                            api_defense_overview
 13565  POST             /api/discord/announce                            api_discord_announce
 13293  GET              /api/discord/clips_week                          api_discord_clips_week
 13509  GET              /api/discord/community                           api_discord_community
 13251  GET              /api/discord/invite                              api_discord_invite
 12825  GET              /api/discord/overview                            api_discord_overview
 12911  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14036  GET              /api/events                                      api_events
 13340  GET              /api/events/stream                               api_events_stream
 14049  GET              /api/forecast/storage                            api_forecast_storage
 12020  GET              /api/freeai/status                               api_freeai_status
 12767  GET              /api/health                                      api_health
 14067  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14063  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20751  GET              /api/highlights                                  api_highlights
 20763  POST             /api/highlights/config                           api_highlights_config
 20859  POST             /api/kickmod/config                              api_kickmod_config
 20904  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20918  GET              /api/kickmod/learned                             api_kickmod_learned
 20945  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20925  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21274  POST             /api/kickmod/say                                 api_kickmod_say
 21250  POST             /api/kickmod/start                               api_kickmod_start
 20830  GET              /api/kickmod/status                              api_kickmod_status
 21261  POST             /api/kickmod/stop                                api_kickmod_stop
 10389  POST             /api/login                                       dashboard_login_submit
 14508  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14477  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13188  GET              /api/notify/status                               api_notify_status
 13199  POST             /api/notify/test                                 api_notify_test
 10613  GET              /api/outcomes                                    api_outcomes
 22152  POST             /api/overlay/config                              api_overlay_config
 22139  POST             /api/overlay/event                               api_overlay_event
 22044  GET              /api/overlay/state                               api_overlay_state
 10646  GET              /api/profile/<username>                          api_profile
 14233  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14075  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14198  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14175  GET              /api/proxy/trend                                 api_proxy_trend
 12475  GET              /api/public/stats                                api_public_stats
 10489  GET              /api/pulse                                       api_pulse
 13643  GET              /api/recording-attempts                          api_recording_attempts
 20359  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20337  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20378  POST             /api/restream/<int:rid>/start                    api_restream_start
 20649  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22006  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20313  POST             /api/restream/create                             api_restream_create
 12600  GET              /api/restream/deck                               api_restream_deck
 11956  GET              /api/restream/health                             api_restream_health
 22028  POST             /api/restream/layout                             api_restream_layout
 20286  GET              /api/restream/list                               api_restream_list
 11925  POST             /api/restream/report                             api_restream_report
 20662  POST             /api/restream/start_all                          api_restream_start_all
 20688  POST             /api/restream/stop_all                           api_restream_stop_all
 12131  GET              /api/restream/testpush                           api_testpush_status
 12156  POST             /api/restream/testpush                           api_testpush_run
 14608  GET              /api/restream/verify                             api_restream_verify
 13271  GET              /api/retention/preview                           api_retention_preview
 13280  POST             /api/retention/run                               api_retention_run
 13992  GET              /api/search                                      api_search
 22880  GET              /api/selftest                                    api_selftest
 20395  GET              /api/shield/stats                                api_shield_stats
 10550  GET              /api/storage                                     api_storage
 10557  POST             /api/storage/cleanup                             api_storage_cleanup
 14129  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11895  GET              /api/stream/timeline                             api_stream_timeline
 12899  GET              /api/stream/transcript                           api_stream_transcript
 10581  GET              /api/summary/preview                             api_summary_preview
 13708  GET              /api/system                                      api_system
 14556  GET              /api/system/check_timing                         api_check_timing
 14671  GET              /api/system/config_drift                         api_config_drift
 12935  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13046  GET              /api/system/preflight                            api_system_preflight
 13172  GET              /api/system/preflight_history                    api_system_preflight_history
 13405  GET              /api/system/resilience                           api_system_resilience
 14027  GET              /api/tags                                        api_tags_list
 10523  GET              /api/top                                         api_top
 10882  GET              /api/trend-7d                                    api_trend_7d
 21075  GET              /api/tts/<fn>                                    api_tts_file
 22180  GET              /api/upload_window                               api_upload_window
 10627  GET              /api/userstats                                   api_userstats
 12523  GET              /api/version                                     api_version
 13681  GET              /archive/<int:eid>/download                      archive_download
 13738  GET              /download/<int:recording_id>                     download
 13621  GET              /health                                          health
 20597  GET              /healthz                                         healthz
 10380  GET              /login                                           dashboard_login_page
 10410  GET              /logout                                          dashboard_logout
 10417  GET              /manifest.webmanifest                            pwa_manifest
 12963  GET              /metrics                                         api_prometheus_metrics
 21989  GET              /overlay                                         overlay_page
 10441  GET              /pwa-icon-<variant>.png                          pwa_icon
 10427  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (206)

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
 23606  /ai                     
 24065  /ask                    
 23697  /assign_role            
 23743  /ban                    
 24397  /botstats               
 24321  /clearwarns             
 24361  /clip                   
 24346  /clipoftheweek          
 24188  /clips                  
 23658  /create_category        
 23627  /create_channel         
 23686  /create_group           
 23669  /create_role            
 23643  /create_voice           
 23979  /daily                  
 24095  /event                  
 24138  /events                 
 24234  /follow                 
 24218  /help                   
 23732  /kick                   
 23961  /leaderboard            
 24174  /livenow                
 24204  /post_test              
 24035  /profile                
 23767  /purge                  
 23947  /rank                   
 24161  /recstatus              
 23708  /remove_role            
 23620  /restream_status        
 23719  /set_channel_perms      
 23912  /setup_community        
 23930  /setup_targets          
 24260  /stats                  
 23532  /status                 
 24556  /streaminfo             
 24453  /sys_report             
 24429  /sys_unpause            
 23754  /timeout                
 24332  /topstreamers           
 23562  /track                  
 23546  /tracklist              
 24249  /unfollow               
 23595  /untrack                
 24282  /warn                   
 24306  /warnings               
```

## Discord-Events (4)

```
 25040  on_member_join
 25002  on_message
 24643  on_raw_reaction_add
 25075  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2496-2497   _abo_key
  2517-2535   _abo_probe_dump
 22422-22432  _active_recorder_sync
 17575-17582  _ad_allowlist
 18702-18708  _agent_for
 22434-22452  _ai_calls_total_sync
 18711-18727  _ai_telemetry
 19209-19227  _alert
 25191-25241  _alert_monitor_loop
 25622-25684  _announce_loop
  3438-3441   _anthropic_key
  3448-3450   _anthropic_model
 10133-10136  _arg_int
  2488-2493   _as_dict
 15352-15357  _audio_cfg
 19363-19385  _audio_tap_cmd
 10301-10312  _auth_cookie
 10268-10297  _auth_guard
  1644-1649   _auto_on
 20262-20280  _auto_restream_loop
 26743-26758  _azrael_broadcast_reply
 26643-26665  _azrael_chat_reply
 26626-26640  _azrael_chat_should_reply
 26671-26673  _azrael_gate_cfg
 18732-18746  _azrael_live_state
 21892-21906  _azrael_overlay_state
 19092-19146  _azrael_proactive_loop
 18551-18607  _azrael_reaction_to_chats
 26676-26683  _azrael_reply_all_chats
 26613-26623  _azrael_self_names
 26711-26740  _azrael_send_to
 18749-18770  _azrael_system
 25360-25363  _backup_active
 25441-25454  _backup_loop
 17463-17464  _badwords_path
 25153-25162  _brain_growth_loop
 10958-10985  _brain_growth_snapshot
  2424-2444   _brain_hint_delay
 10950-10952  _brain_history_for
  6517-6545   _brain_notify
 10927-10948  _brain_record
 10954-10956  _brain_stream_recent
 13319-13336  _browser_push
  6561-6648   _build_daily_summary
  2927-3107   _build_native_cmd
 15713-15900  _build_restream_cmd
  3151-3184   _build_ytdlp_cmd
 22374-22381  _cached_probe
  5339-5366   _can_stop_tracking
  1824-1846   _capture_set_cookies
 14292-14295  _cfg_get
 14298-14300  _cfg_set
 21636-21671  _channel_set_all
 14950-14953  _chat_connected
 14956-14972  _chat_disconnected
  8613-8624   _chat_is_forum
 14992-14994  _chat_sanitize
 14996-15005  _chat_src_ok
 14935-14947  _chat_stat
 14975-14978  _chat_stats_snapshot
  3713-3724   _check_ai_alive_sync
  3727-3739   _check_ai_models_sync
 22383-22396  _check_redis_alive_sync
 22398-22418  _check_redis_version_sync
 11557-11600  _classify_pool_anonymity
 11603-11620  _classify_pool_anonymity_bg
   802-806    _claude_chat_sync_metered
 10162-10169  _client_ip
 25716-25743  _clip_prune
 25746-25756  _clip_recfile_for
 26272-26278  _clip_should_velocity
 25797-25879  _clip_to_discord
  3611-3620   _close_ai_session
 26787-26802  _cohost_broadcast
 26769-26773  _cohost_cfg
 26828-26840  _cohost_fire_highlight
 26776-26784  _cohost_gate
 26805-26825  _cohost_highlight
 25928-25962  _community_events_loop
 10781-10783  _conv_messages
  6925-6968   _cookie_alarm_loop
  1896-1900   _cookie_autorefresh_info
  1801-1805   _cookie_header
 13369-13401  _cpu_load_snapshot
  3921-3933   _create_index_safe
 22635-22741  _crowdsec_status
 22601-22632  _crowdsec_via_lapi
 22466-22484  _cscli_bin
 22490-22503  _cscli_path
  6815-6840   _daily_summary_loop
 22521-22538  _darf_journal_lesen
 25165-25188  _db_maintenance_loop
  6784-6812   _db_vacuum_loop
 17598-17622  _detect_foreign_ad
  1382-1393   _diag_path_owner
 18998-19042  _director_finalize
 19809-19816  _director_for
 18947-18995  _director_mark
 26166-26201  _disc_automod_check
 26139-26145  _disc_state_get
 26148-26155  _disc_state_set
 23184-23197  _discord_guild_filesize_bytes
 23383-23392  _discord_invite
 26100-26136  _discord_live_thread
 19149-19161  _discord_notify
 23284-23309  _discord_ops_alert
 25998-26096  _discord_post_user
 23448-25150  _discord_run_once
 23322-23380  _discord_start
 25687-25693  _discord_stop
 23205-23207  _discord_upload_limit_label
 23200-23202  _discord_upload_limit_mb
  6843-6920   _disk_alarm_loop
 28194-28243  _disk_autoclean
 28246-28259  _disk_guard_loop
 28186-28191  _disk_pct
 15309-15311  _drawtext_chain
 13835-13837  _dump_all_threads
 11482-11546  _enrich_proxies_with_geo
  2041-2085   _ensure_cookie_file_netscape
 23395-23445  _ensure_discord_invite
 25893-25925  _ensure_error_channel
  8672-8675   _ensure_notify_topic
 11727-11764  _ensure_proxy_ready
  8626-8653   _ensure_topic
   659-661    _env_int
   664-666    _env_int_range
 25965-25995  _error_channel_loop
 19193-19206  _event_webhook
 14758-14771  _evolution_loop
  5959-5993   _extract_file_payload
  2173-2175   _extract_urls_from_streamurl_node
 22506-22513  _f2b_sudo_hint
 19229-19231  _faster_whisper_available
 17487-17499  _fetch_ldnoobw_de
 11371-11389  _fetch_proxy_list
 19643-19671  _fetch_tiktok_room_id
   735-738    _ff_cmd
 15472-15477  _find_chromium
  3144-3148   _find_external_recorder
  2178-2180   _find_stream_urls
 14343-14368  _fire_webhooks
  7704-7713   _fork_safe
   817-826    _freeai_chat_sync_metered
 22556-22598  _geo_lookup_ips
  3600-3609   _get_ai_session
  7538-7578   _get_live_info
  2714-2721   _get_resolve_semaphore
  7968-8334   _handle_single_tracking
 28038-28040  _hb
 28043-28060  _hb_while
 15010-15012  _highlight_cfg
 15015-15044  _highlight_observe
 15480-15498  _htmlov_screenshot_cmd
 19387-19397  _httpx_proxy
 14376-14388  _in_quiet_hours
 29073-29104  _install_fast_eventloop
 10028-10082  _install_fast_json
 13840-13856  _install_faulthandler
 20505-20514  _intel_ensure_schema
 20552-20587  _intel_index_loop
 20526-20536  _intel_index_one
 20517-20523  _intel_semantic
  5328-5337   _is_authorized
  7869-7875   _is_dead
  2163-2165   _is_hevc
 22541-22547  _is_private_ip
  1546-1553   _is_process_running
  6547-6558   _is_quiet_hours
  1183-1192   _is_upload_window
 10117-10130  _json_error_handler
  6770-6771   _kick_broadcaster_id
 12057-12076  _kick_channel_live
  6682-6724   _kick_follower_count
  6666-6669   _kick_slug
 12550-12581  _kick_user_token
  3970-3973   _kind_from_filename
 14405-14410  _latest_popularity
 17509-17515  _learned_load
 17506-17507  _learned_path
 17517-17525  _learned_save
 20024-20057  _live_react_loop
 19820-20013  _live_react_worker
 18610-18621  _live_transcript_push
 20015-20022  _live_users
 19045-19089  _living_title_loop
 17466-17474  _load_banned_words_file
  1722-1795   _load_cookies_dict
 25366-25438  _local_backup_scan
 10099-10113  _log_5xx
 15908-15920  _looks_like_codec_err
 15903-15905  _looks_like_source_expired
  7785-7815   _loop_fehler
 13860-13869  _loop_heartbeat
 28008-28035  _loop_lag_monitor
 13872-13940  _loop_watchdog_thread
 18490-18504  _loyalty_add
 18481-18487  _loyalty_get
 18507-18515  _loyalty_top
 14542-14544  _manual_donations_total
  7877-7878   _mark_dead
 12228-12244  _marketing_loop
 26690-26708  _maybe_handle_command
 28345-28369  _maybe_hype_clip
  3888-3911   _migrate_columns
 26967-26978  _mod_is_exempt
 26981-26986  _mod_warn_first
 26989-26992  _mod_warn_text
 14798-14806  _modlog
   936-938    _multistream_targets
  7716-7717   _nc_create_subprocess_exec
  7720-7721   _nc_create_subprocess_shell
 12480-12497  _news_loop
 14836-14838  _normalize_ingest
  2355-2372   _note_check_duration
  8666-8669   _notify_topic_name
 18636-18644  _oracle_memories
 18902-18936  _oracle_memorize
 18647-18660  _oracle_persona
 18629-18633  _oracle_recent_text
 15135-15143  _ov_atomic_write
 15123-15129  _ov_bar
 17422-17434  _ov_clip_text
 15132-15133  _ov_oneline
 21956-21985  _overlay_push
 15426-15469  _overlay_render_size
 14897-14901  _overlay_session_reset
 21908-21911  _overlay_src_ok
 17585-17595  _own_invites
 15421-15423  _parse_size
 22749-22829  _parse_ssh_attacks
  7140-7173   _pause_resume_cmd
  1850-1894   _persist_refreshed_cookies
  1688-1720   _pick_checked_pull_proxy
 10198-10211  _pin_auth_value
 10257-10258  _pin_clear_fail
 10237-10240  _pin_locked
 10243-10254  _pin_note_fail
 10214-10234  _pin_ok
 21798-21800  _piper_available
 21763-21785  _piper_list_voices
 21805-21830  _piper_pick_model
 21842-21889  _piper_say
 21756-21760  _piper_voice_roots
 14305-14340  _post_json_threaded
 15400-15418  _probe_video_size
  1574-1591   _proc_is_recorder
 11469-11480  _proxy_geo_cache_put
 11696-11724  _proxy_pool_refresh_loop
  1654-1685   _proxy_report_recording
 13825-13827  _prune_stall_dumps
 12298-12419  _public_stats
 19164-19190  _push_notify
 10359-10361  _pwa_dir
 11440-11455  _quick_validate_proxy
 14371-14373  _quiet_hours_config
 10324-10357  _rate_guard
 18455-18461  _react_warn
  7624-7663   _reap_proc
  2395-2417   _record_check_outcome
   730-732    _redact_stream_urls
 11623-11693  _refresh_proxy_pool
 21788-21794  _resolve_piper_model
  2189-2279   _resolve_via_html
  2537-2691   _resolve_via_webcast_api_v2
  2754-2816   _resolve_via_ytdlp
 26317-26446  _resolve_youtube_ingest
 20096-20103  _restream_active_platforms
 14882-14893  _restream_active_sources
 19674-19773  _restream_chat_guardian
 15047-15119  _restream_chat_push
 14809-14821  _restream_enabled
 15501-15588  _restream_html_overlay_start
 15591-15604  _restream_html_overlay_stop
  1131-1133   _restream_layout_mode
 14847-14870  _restream_overlay_files
 20061-20093  _restream_platform_state
 20224-20259  _restream_resume_after_restart
 15652-15710  _restream_tts_enqueue_wav
 15362-15394  _restream_tts_feeder
 15359-15360  _restream_tts_fifo_path
 15607-15634  _restream_tts_start
 15636-15650  _restream_tts_stop
 20106-20221  _restream_verify_loop
 25331-25343  _retention_loop
 25290-25328  _retention_scan
  2499-2501   _room_is_abo
  5997-6114   _run_ai_call
 13963-13976  _run_async_from_flask
 22550-22553  _run_priv
 29061-29069  _run_selfcheck_and_exit
 25346-25357  _s3_client
  7904-7955   _safe_send
  4592-4608   _sample_net_throughput
 17476-17484  _save_banned_words_file
  2447-2474   _schedule_next_check
 25244-25287  _scheduler_loop
  3914-3918   _schema_pk
 13980-13985  _scraper_session
 26995-27034  _screen_full
 12783-12820  _sec_headers
  2168-2170   _select_stream_from_data_section
 28874-29058  _selfcheck
  8678-8712   _send_live_notice
  1206-1210   _should_defer_upload
 25759-25794  _shrink_for_discord
 10364-10376  _sicheres_ziel
 28266-28283  _sign_health_check
 28286-28305  _sign_health_loop
  7733-7744   _spawn
  7747-7777   _spawn_from_flask
 22873-22876  _st_befund
 19399-19640  _start_chat_listener
 13943-13960  _start_loop_watchdog
 12443-12471  _stats_loop
 12422-12425  _stats_output_path
 12428-12440  _stats_write
  8406-8422   _storage_cleanup_loop
 28325-28332  _story_for
  3206-3212   _stream_url_expiry
  3221-3227   _stream_url_is_fresh
  3214-3219   _stream_url_ttl
 17549-17556  _streamer_persona_get
 17531-17537  _streamer_personas_load
 17528-17529  _streamer_personas_path
 17539-17547  _streamer_personas_save
 15314-15318  _studio_chain
 25463-25585  _system_backup
 25588-25618  _system_backup_loop
 11392-11431  _test_proxy
 12098-12107  _testpush_cfg
 12110-12127  _testpush_exec
 12079-12095  _testpush_resolve_live
  7880-7901   _tg_sprache_setzen
  8585-8595   _tg_topics_load_into_mem
  8582-8583   _tg_topics_path
  8597-8604   _tg_topics_save
 10172-10180  _token_ok
  8607-8611   _topic_forget
 14391-14402  _tracking_max_duration
  4179-4193   _tracking_remove_cleanup
  4210-4222   _tracking_resume_cleanup
  1440-1463   _try_attach_file_handler
 21832-21840  _tts_cleanup
 12035-12039  _tunnel_effective
 21295-21348  _twitch_channel_status
 27037-27180  _twitch_chat_loop
 26851-26954  _twitch_eventsub_loop
  1229-1242   _upload_queue_add
  1253-1255   _upload_queue_count
  1212-1221   _upload_queue_load
  1202-1204   _upload_queue_path
  1244-1251   _upload_queue_remove
  1223-1227   _upload_queue_save
  1257-1298   _upload_window_loop
  7597-7604   _uptime_s
 14824-14833  _url_host
   710-727    _url_ohne_zugang
   795-799    _usage_record_claude
  7818-7862   _verbindung_verloren
  6727-6758   _viewer_sample_loop
  6774-6781   _viewer_stats
 10261-10264  _wants_html
  7607-7621   _warn_empty_env
 28081-28176  _watchdog_loop
 26592-26600  _wchat_thank_ok
 19233-19263  _whisper_get_model
  7694-7701   _whisper_native_section
 18442-18448  _whisper_pool
 19332-19361  _whisper_segments
 19265-19329  _whisper_transcribe
 15145-15307  _write_restream_overlay
 27208-27287  _youtube_api_chat_loop
 21351-21454  _youtube_api_status
 21457-21524  _youtube_channel_status
 27290-27450  _youtube_chat_loop
 26452-26465  _youtube_restream_autoconfig
 26468-26492  _youtube_restream_autoconfig_inner
 26559-26587  _youtube_send
 21592-21633  _youtube_set_channel
 26495-26529  _yt_access_token
 26532-26547  _yt_live_chat_id
 27201-27205  _yt_oauth_configured
 26555-26556  _yt_sendrate_cfg
 27183-27198  _yt_timeout
  2738-2739   _ytdlp_detect_available
  2741-2752   _ytdlp_note_result
 13830-13832  _zombie_child_count
  7474-7498   about
  4089-4093   add_ai_log_entry
  4006-4009   add_archive_entry
  4705-4720   add_archive_rule
  4381-4415   add_recording
  4154-4171   add_tracking
  6117-6150   ai
  3753-3792   ai_chat
  3826-3836   ai_history_append
  3838-3843   ai_history_clear
  3815-3824   ai_history_load
  3800-3813   ai_rate_limit_check
  6179-6187   aireset
 18773-18792  azrael_chat
 27455-27577  brain_cmd
  3230-3414   build_recording_cmd
  4174-4177   bulk_add_trackings
  6971-7030   bulkadd
  8425-8565   check_all_trackings
  4226-4238   claim_live_transition
 17625-18380  class KickModerator
 15923-17309  class RestreamManager
 11809-11851  classify_proxy_anonymity
  6225-6423   cleanup
  5188-5229   cleanup_old_recordings
  4372-4379   clear_recording
 26204-26269  clip_moment
  4536-4585   compute_storage_forecast
  7093-7137   cookies_cmd
  4145-4151   count_trackings_for_chat
  4076-4087   decide_preferred_recorder
  4016-4019   delete_archive_entry
  4722-4730   delete_archive_rule
  5654-5801   diag
 27689-27750  einnahmen_cmd
  4530-4533   find_recordings_by_fingerprint
  4037-4053   finish_recording_attempt
  4198-4200   get_all_active_trackings
  4104-4107   get_all_checks
  4417-4420   get_all_recordings
  4479-4481   get_all_tags_with_counts
  4507-4510   get_annotations_for_recording
  4011-4014   get_archive_entry
  4500-4503   get_bookmarked_recordings
  1917-2034   get_cookie_health
  4467-4473   get_event_log
  4060-4074   get_last_recording_attempt
  2819-2924   get_live_status
  4988-4991   get_manual_recordings
  4515-4518   get_or_compute_inspect_sync
  5264-5308   get_outcome_breakdown
  4486-4489   get_priority_poll_interval
  4683-4692   get_profile_snapshots
  4055-4058   get_recent_recording_attempts
  4422-4425   get_recording_by_id
  4493-4496   get_recording_note
  3548-3571   get_redis
  4134-4137   get_stats
  5155-5186   get_storage_stats
  4823-4825   get_tiktok_status_distribution
  4240-4249   get_tracking_state
  4195-4196   get_trackings_for_group
  5004-5007   get_trash_recordings
  9333-9996   handle_recording_finished
  3936-3961   init_db
  5078-5132   inspect_stream_url
 21951-21953  is_revenue_platform
  4695-4703   list_archive_rules
  5458-5496   live
  7958-7966   live_check_worker
  3623-3657   llm_chat
  3680-3708   llm_chat_sync
  3665-3677   llm_list_models
  4433-4459   log_event
  1508-1541   log_recording_failure
  7287-7336   logs_cmd
 28373-28864  main
  6153-6176   on_ai_media
  7413-7439   on_ai_reply
  7442-7471   on_azrael_mention
  7503-7533   on_callback
 18795-18899  oracle_handle
  7176-7179   pause_tracking
  5318-5323   profile_keyboard
  7238-7284   quota
  8336-8403   reaper_loop
  4819-4821   record_tiktok_status
  6192-6222   recstatus
  3573-3581   redis_get_json
  3583-3589   redis_set_json
 27753-27763  report_cmd
 11854-11856  report_proxy_result
  2282-2309   resolve_tiktok_live_stream
  4999-5002   restore_recording
  7182-7185   resume_tracking
  4733-4813   run_archive_rules
 27766-27988  run_bot
 13752-13799  run_flask
  4611-4656   sample_bandwidth_for_active
  4662-4681   save_profile_snapshot
  4096-4102   save_tiktok_check
  4364-4370   set_recording_file
  4203-4207   set_tracking_paused
  4994-4997   soft_delete_recording
  8718-9331   split_and_send_video
  5371-5413   start
  4021-4035   start_recording_attempt
  6426-6464   stats
  4969-4986   stop_manual_recording
  7188-7235   stoprec
  6651-6659   summary_cmd
  7339-7410   sysres
  5803-5947   teststream
  5415-5456   tiktok
  7033-7090   topusers
  5533-5590   track
  5498-5530   track_exact
  5604-5652   tracklist
  4835-4967   trigger_manual_recording
  4325-4362   try_acquire_recording_lock
  5010-5069   universal_search
  5592-5602   untrack
 27580-27686  update_cmd
  4525-4528   update_recording_fingerprint
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
claude.py              api_key, build_payload, chat_sync, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              decide, default_config, new_state, prompt_seed, snapshot
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
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, url_host
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
