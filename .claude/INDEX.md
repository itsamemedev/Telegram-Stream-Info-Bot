# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (161)

```
 10475  GET              /                                                dashboard
 14271  GET              /api/abo/status                                  api_abo_status
 10548  GET              /api/active-recordings                           api_active_recordings
 14342  GET              /api/activity-pulse                              api_activity_pulse
 14149  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20819  GET/POST         /api/audio/config                                api_audio_config
 20849  POST             /api/audio/testtone                              api_audio_testtone
 14215  GET/POST         /api/auto-archive-rules                          api_archive_rules
 14239  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 14243  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 12002  GET              /api/automation/status                           api_automation_status
 12024  POST             /api/automation/toggle                           api_automation_toggle
 13146  GET              /api/azrael/agents                               api_azrael_agents
 11894  POST             /api/azrael/ask                                  api_azrael_ask
 21055  GET/POST         /api/azrael/context                              api_azrael_context
 12851  GET              /api/azrael/core                                 api_azrael_core
 21189  POST             /api/azrael/live_pause                           api_azrael_live_pause
 21179  GET              /api/azrael/live_status                          api_azrael_live_status
 21197  POST             /api/azrael/live_test                            api_azrael_live_test
 13155  GET              /api/azrael/memories                             api_azrael_memories
 21245  POST             /api/azrael/persona                              api_azrael_persona_set
 21236  GET              /api/azrael/personas                             api_azrael_personas
 21273  GET              /api/azrael/piper_status                         api_azrael_piper_status
 21028  POST             /api/azrael/react                                api_azrael_react
 21064  GET              /api/azrael/reaction                             api_azrael_reaction
 21216  GET              /api/azrael/reactions                            api_azrael_reactions
 21266  GET              /api/azrael/transcript                           api_azrael_transcript
 21151  POST             /api/azrael/tts_test                             api_azrael_tts_test
 21126  GET              /api/azrael/voices                               api_azrael_voices
 21290  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10847  GET              /api/backoff-watch                               api_backoff_watch
 13630  POST             /api/backup/run                                  api_backup_run
 13596  GET              /api/backup/status                               api_backup_status
 13585  POST             /api/backup/system                               api_backup_system
 14181  GET              /api/bandwidth/live                              api_bandwidth_live
 14134  GET              /api/bookmarks                                   api_bookmarks_list
 11110  GET              /api/brain                                       api_brain
 11047  GET              /api/brain/alarms                                api_brain_alarms
 11032  GET              /api/brain/creator                               api_brain_creator
 11009  GET              /api/brain/graph                                 api_brain_graph
 11070  GET              /api/brain/growth                                api_brain_growth
 10025  GET              /api/brain/health                                api_brain_health
 21771  GET              /api/channel/categories                          api_channel_categories
 21777  POST             /api/channel/set                                 api_channel_set
 21587  GET              /api/channels/status                             api_channels_status
 20463  POST             /api/chat/send                                   api_chat_send
 13350  GET              /api/chat/send_status                            api_chat_send_status
 10529  GET              /api/checks                                      api_checks
 21092  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 21075  GET              /api/clips                                       api_clips
 21108  POST/DELETE      /api/clips/clear                                 api_clips_clear
 20741  GET              /api/cohost                                      api_cohost
 20753  POST             /api/cohost/config                               api_cohost_config
 14650  GET              /api/community/stats                             api_community_stats
 22411  GET              /api/data/export                                 api_data_export
 20667  GET              /api/debug/threads                               api_debug_threads
 23238  GET              /api/defense/attacks                             api_defense_attacks
 23205  GET              /api/defense/crowdsec                            api_defense_crowdsec
 23223  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22929  GET              /api/defense/overview                            api_defense_overview
 13692  POST             /api/discord/announce                            api_discord_announce
 13420  GET              /api/discord/clips_week                          api_discord_clips_week
 13636  GET              /api/discord/community                           api_discord_community
 13378  GET              /api/discord/invite                              api_discord_invite
 12952  GET              /api/discord/overview                            api_discord_overview
 13038  POST             /api/discord/webhook_test                        api_discord_webhook_test
 14163  GET              /api/events                                      api_events
 13467  GET              /api/events/stream                               api_events_stream
 14176  GET              /api/forecast/storage                            api_forecast_storage
 12040  GET              /api/freeai/status                               api_freeai_status
 12894  GET              /api/health                                      api_health
 14194  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 14190  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20790  GET              /api/highlights                                  api_highlights
 20802  POST             /api/highlights/config                           api_highlights_config
 21628  GET              /api/kick/channel                                api_kick_channel
 21649  POST             /api/kick/channel                                api_kick_channel_set
 12651  GET              /api/kick/oauth/callback                         api_kick_oauth_callback
 12719  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect
 12697  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect
 12636  GET              /api/kick/oauth/start                            api_kick_oauth_start
 12676  GET              /api/kick/oauth/status                           api_kick_oauth_status
 20867  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck
 20936  POST             /api/kickmod/config                              api_kickmod_config
 20981  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20995  GET              /api/kickmod/learned                             api_kickmod_learned
 21022  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 21002  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 21333  POST             /api/kickmod/say                                 api_kickmod_say
 21309  POST             /api/kickmod/start                               api_kickmod_start
 20907  GET              /api/kickmod/status                              api_kickmod_status
 21320  POST             /api/kickmod/stop                                api_kickmod_stop
 10409  POST             /api/login                                       dashboard_login_submit
 14635  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14604  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13315  GET              /api/notify/status                               api_notify_status
 13326  POST             /api/notify/test                                 api_notify_test
 10633  GET              /api/outcomes                                    api_outcomes
 22248  POST             /api/overlay/config                              api_overlay_config
 22235  POST             /api/overlay/event                               api_overlay_event
 22140  GET              /api/overlay/state                               api_overlay_state
 10666  GET              /api/profile/<username>                          api_profile
 14360  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 14202  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 14325  GET              /api/proxy/heatmap                               api_proxy_heatmap
 14302  GET              /api/proxy/trend                                 api_proxy_trend
 12495  GET              /api/public/stats                                api_public_stats
 10509  GET              /api/pulse                                       api_pulse
 13770  GET              /api/recording-attempts                          api_recording_attempts
 20398  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20376  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20417  POST             /api/restream/<int:rid>/start                    api_restream_start
 20688  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 22102  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20352  POST             /api/restream/create                             api_restream_create
 12727  GET              /api/restream/deck                               api_restream_deck
 11976  GET              /api/restream/health                             api_restream_health
 22124  POST             /api/restream/layout                             api_restream_layout
 20325  GET              /api/restream/list                               api_restream_list
 11945  POST             /api/restream/report                             api_restream_report
 20701  POST             /api/restream/start_all                          api_restream_start_all
 20727  POST             /api/restream/stop_all                           api_restream_stop_all
 12151  GET              /api/restream/testpush                           api_testpush_status
 12176  POST             /api/restream/testpush                           api_testpush_run
 14735  GET              /api/restream/verify                             api_restream_verify
 13398  GET              /api/retention/preview                           api_retention_preview
 13407  POST             /api/retention/run                               api_retention_run
 14119  GET              /api/search                                      api_search
 22976  GET              /api/selftest                                    api_selftest
 20434  GET              /api/shield/stats                                api_shield_stats
 10570  GET              /api/storage                                     api_storage
 10577  POST             /api/storage/cleanup                             api_storage_cleanup
 14256  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11915  GET              /api/stream/timeline                             api_stream_timeline
 13026  GET              /api/stream/transcript                           api_stream_transcript
 10601  GET              /api/summary/preview                             api_summary_preview
 13835  GET              /api/system                                      api_system
 14683  GET              /api/system/check_timing                         api_check_timing
 14798  GET              /api/system/config_drift                         api_config_drift
 13062  GET              /api/system/config_snapshot                      api_system_config_snapshot
 13173  GET              /api/system/preflight                            api_system_preflight
 13299  GET              /api/system/preflight_history                    api_system_preflight_history
 13532  GET              /api/system/resilience                           api_system_resilience
 14154  GET              /api/tags                                        api_tags_list
 10543  GET              /api/top                                         api_top
 10902  GET              /api/trend-7d                                    api_trend_7d
 21140  GET              /api/tts/<fn>                                    api_tts_file
 22276  GET              /api/upload_window                               api_upload_window
 10647  GET              /api/userstats                                   api_userstats
 12543  GET              /api/version                                     api_version
 13808  GET              /archive/<int:eid>/download                      archive_download
 13865  GET              /download/<int:recording_id>                     download
 13748  GET              /health                                          health
 20636  GET              /healthz                                         healthz
 10400  GET              /login                                           dashboard_login_page
 10430  GET              /logout                                          dashboard_logout
 10437  GET              /manifest.webmanifest                            pwa_manifest
 13090  GET              /metrics                                         api_prometheus_metrics
 22085  GET              /overlay                                         overlay_page
 10461  GET              /pwa-icon-<variant>.png                          pwa_icon
 10447  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (198)

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
 23702  /ai                     
 24161  /ask                    
 23793  /assign_role            
 23839  /ban                    
 24493  /botstats               
 24417  /clearwarns             
 24457  /clip                   
 24442  /clipoftheweek          
 24284  /clips                  
 23754  /create_category        
 23723  /create_channel         
 23782  /create_group           
 23765  /create_role            
 23739  /create_voice           
 24075  /daily                  
 24191  /event                  
 24234  /events                 
 24330  /follow                 
 24314  /help                   
 23828  /kick                   
 24057  /leaderboard            
 24270  /livenow                
 24300  /post_test              
 24131  /profile                
 23863  /purge                  
 24043  /rank                   
 24257  /recstatus              
 23804  /remove_role            
 23716  /restream_status        
 23815  /set_channel_perms      
 24008  /setup_community        
 24026  /setup_targets          
 24356  /stats                  
 23628  /status                 
 24652  /streaminfo             
 24549  /sys_report             
 24525  /sys_unpause            
 23850  /timeout                
 24428  /topstreamers           
 23658  /track                  
 23642  /tracklist              
 24345  /unfollow               
 23691  /untrack                
 24378  /warn                   
 24402  /warnings               
```

## Discord-Events (4)

```
 25136  on_member_join
 25098  on_message
 24739  on_raw_reaction_add
 25171  on_ready
```

## Top-Level-Symbole in bot.py (515 Funktionen, 2 Klassen)

```
  2491-2492   _abo_key
  2512-2530   _abo_probe_dump
 22518-22528  _active_recorder_sync
 17619-17626  _ad_allowlist
 18741-18747  _agent_for
 22530-22548  _ai_calls_total_sync
 18750-18766  _ai_telemetry
 19248-19266  _alert
 25287-25337  _alert_monitor_loop
 25718-25780  _announce_loop
  3433-3436   _anthropic_key
  3443-3445   _anthropic_model
 10153-10156  _arg_int
  2483-2488   _as_dict
 15479-15484  _audio_cfg
 19402-19424  _audio_tap_cmd
 10321-10332  _auth_cookie
 10288-10317  _auth_guard
  1639-1644   _auto_on
 20301-20319  _auto_restream_loop
 26839-26854  _azrael_broadcast_reply
 26739-26761  _azrael_chat_reply
 26722-26736  _azrael_chat_should_reply
 26767-26769  _azrael_gate_cfg
 18771-18785  _azrael_live_state
 21988-22002  _azrael_overlay_state
 19131-19185  _azrael_proactive_loop
 18590-18646  _azrael_reaction_to_chats
 26772-26779  _azrael_reply_all_chats
 26709-26719  _azrael_self_names
 26807-26836  _azrael_send_to
 18788-18809  _azrael_system
 25456-25459  _backup_active
 25537-25550  _backup_loop
 17507-17508  _badwords_path
 25249-25258  _brain_growth_loop
 10978-11005  _brain_growth_snapshot
  2419-2439   _brain_hint_delay
 10970-10972  _brain_history_for
  6512-6540   _brain_notify
 10947-10968  _brain_record
 10974-10976  _brain_stream_recent
 13446-13463  _browser_push
  6556-6643   _build_daily_summary
  2922-3102   _build_native_cmd
 15827-16014  _build_restream_cmd
  3146-3179   _build_ytdlp_cmd
 22470-22477  _cached_probe
  5334-5361   _can_stop_tracking
  1819-1841   _capture_set_cookies
 14419-14422  _cfg_get
 14425-14427  _cfg_set
 21732-21767  _channel_set_all
 15077-15080  _chat_connected
 15083-15099  _chat_disconnected
  8633-8644   _chat_is_forum
 15119-15121  _chat_sanitize
 15123-15132  _chat_src_ok
 15062-15074  _chat_stat
 15102-15105  _chat_stats_snapshot
  3708-3719   _check_ai_alive_sync
  3722-3734   _check_ai_models_sync
 22479-22492  _check_redis_alive_sync
 22494-22514  _check_redis_version_sync
 11577-11620  _classify_pool_anonymity
 11623-11640  _classify_pool_anonymity_bg
   797-801    _claude_chat_sync_metered
 10182-10189  _client_ip
 25812-25839  _clip_prune
 25842-25852  _clip_recfile_for
 26368-26374  _clip_should_velocity
 25893-25975  _clip_to_discord
  3606-3615   _close_ai_session
 26883-26898  _cohost_broadcast
 26865-26869  _cohost_cfg
 26924-26936  _cohost_fire_highlight
 26872-26880  _cohost_gate
 26901-26921  _cohost_highlight
 26024-26058  _community_events_loop
 10801-10803  _conv_messages
  6945-6988   _cookie_alarm_loop
  1891-1895   _cookie_autorefresh_info
  1796-1800   _cookie_header
 13496-13528  _cpu_load_snapshot
  3916-3928   _create_index_safe
 22731-22837  _crowdsec_status
 22697-22728  _crowdsec_via_lapi
 22562-22580  _cscli_bin
 22586-22599  _cscli_path
  6835-6860   _daily_summary_loop
 22617-22634  _darf_journal_lesen
 25261-25284  _db_maintenance_loop
  6804-6832   _db_vacuum_loop
 17642-17666  _detect_foreign_ad
  1377-1388   _diag_path_owner
 19037-19081  _director_finalize
 19848-19855  _director_for
 18986-19034  _director_mark
 26262-26297  _disc_automod_check
 26235-26241  _disc_state_get
 26244-26251  _disc_state_set
 23280-23293  _discord_guild_filesize_bytes
 23479-23488  _discord_invite
 26196-26232  _discord_live_thread
 19188-19200  _discord_notify
 23380-23405  _discord_ops_alert
 26094-26192  _discord_post_user
 23544-25246  _discord_run_once
 23418-23476  _discord_start
 25783-25789  _discord_stop
 23301-23303  _discord_upload_limit_label
 23296-23298  _discord_upload_limit_mb
  6863-6940   _disk_alarm_loop
 28290-28339  _disk_autoclean
 28342-28355  _disk_guard_loop
 28282-28287  _disk_pct
 15436-15438  _drawtext_chain
 13962-13964  _dump_all_threads
 11502-11566  _enrich_proxies_with_geo
  2036-2080   _ensure_cookie_file_netscape
 23491-23541  _ensure_discord_invite
 25989-26021  _ensure_error_channel
  8692-8695   _ensure_notify_topic
 11747-11784  _ensure_proxy_ready
  8646-8673   _ensure_topic
   655-657    _env_int
   660-662    _env_int_range
 26061-26091  _error_channel_loop
 19232-19245  _event_webhook
 14885-14898  _evolution_loop
  5954-5988   _extract_file_payload
  2168-2170   _extract_urls_from_streamurl_node
 22602-22609  _f2b_sudo_hint
 19268-19270  _faster_whisper_available
 17531-17543  _fetch_ldnoobw_de
 11391-11409  _fetch_proxy_list
 19682-19710  _fetch_tiktok_room_id
   731-734    _ff_cmd
 15599-15604  _find_chromium
  3139-3143   _find_external_recorder
  2173-2175   _find_stream_urls
 14470-14495  _fire_webhooks
  7724-7733   _fork_safe
   812-821    _freeai_chat_sync_metered
 22652-22694  _geo_lookup_ips
  3595-3604   _get_ai_session
  7558-7598   _get_live_info
  2709-2716   _get_resolve_semaphore
  7988-8354   _handle_single_tracking
 28134-28136  _hb
 28139-28156  _hb_while
 15137-15139  _highlight_cfg
 15142-15171  _highlight_observe
 15607-15612  _htmlov_screenshot_cmd
 19426-19436  _httpx_proxy
 14503-14515  _in_quiet_hours
 29169-29200  _install_fast_eventloop
 10048-10102  _install_fast_json
 13967-13983  _install_faulthandler
 20544-20553  _intel_ensure_schema
 20591-20626  _intel_index_loop
 20565-20575  _intel_index_one
 20556-20562  _intel_semantic
  5323-5332   _is_authorized
  7889-7895   _is_dead
  2158-2160   _is_hevc
 22637-22643  _is_private_ip
  1541-1548   _is_process_running
  6542-6553   _is_quiet_hours
  1178-1187   _is_upload_window
 10137-10150  _json_error_handler
  6762-6792   _kick_broadcaster_id
 12077-12096  _kick_channel_live
  6676-6718   _kick_follower_count
 12614-12627  _kick_oauth_exchange
 12630-12632  _kick_oauth_page
 12576-12577  _kick_redirect_public
 12572-12573  _kick_redirect_source
 12564-12569  _kick_redirect_uri
  6661-6663   _kick_slug
 12580-12611  _kick_user_token
  3965-3968   _kind_from_filename
 14532-14537  _latest_popularity
 17553-17559  _learned_load
 17550-17551  _learned_path
 17561-17569  _learned_save
 20063-20096  _live_react_loop
 19859-20052  _live_react_worker
 18649-18660  _live_transcript_push
 20054-20061  _live_users
 19084-19128  _living_title_loop
 17510-17518  _load_banned_words_file
  1717-1790   _load_cookies_dict
 25462-25534  _local_backup_scan
 10119-10133  _log_5xx
 16022-16034  _looks_like_codec_err
 16017-16019  _looks_like_source_expired
  7805-7835   _loop_fehler
 13987-13996  _loop_heartbeat
 28104-28131  _loop_lag_monitor
 13999-14067  _loop_watchdog_thread
 18529-18543  _loyalty_add
 18520-18526  _loyalty_get
 18546-18554  _loyalty_top
 14669-14671  _manual_donations_total
  7897-7898   _mark_dead
 12248-12264  _marketing_loop
 26786-26804  _maybe_handle_command
 28441-28465  _maybe_hype_clip
  3883-3906   _migrate_columns
 27063-27074  _mod_is_exempt
 27077-27082  _mod_warn_first
 27085-27088  _mod_warn_text
 14925-14933  _modlog
   931-933    _multistream_targets
  7736-7737   _nc_create_subprocess_exec
  7740-7741   _nc_create_subprocess_shell
 12500-12517  _news_loop
 14963-14965  _normalize_ingest
  2350-2367   _note_check_duration
  8686-8689   _notify_topic_name
 18675-18683  _oracle_memories
 18941-18975  _oracle_memorize
 18686-18699  _oracle_persona
 18668-18672  _oracle_recent_text
 15262-15270  _ov_atomic_write
 15250-15256  _ov_bar
 17466-17478  _ov_clip_text
 15259-15260  _ov_oneline
 22052-22081  _overlay_push
 15553-15596  _overlay_render_size
 15024-15028  _overlay_session_reset
 22004-22007  _overlay_src_ok
 17629-17639  _own_invites
 15548-15550  _parse_size
 22845-22925  _parse_ssh_attacks
  7160-7193   _pause_resume_cmd
  1845-1889   _persist_refreshed_cookies
  1683-1715   _pick_checked_pull_proxy
 10218-10231  _pin_auth_value
 10277-10278  _pin_clear_fail
 10257-10260  _pin_locked
 10263-10274  _pin_note_fail
 10234-10254  _pin_ok
 21894-21896  _piper_available
 21859-21881  _piper_list_voices
 21901-21926  _piper_pick_model
 21938-21985  _piper_say
 21852-21856  _piper_voice_roots
 14432-14467  _post_json_threaded
 15527-15545  _probe_video_size
  1569-1586   _proc_is_recorder
 11489-11500  _proxy_geo_cache_put
 11716-11744  _proxy_pool_refresh_loop
  1649-1680   _proxy_report_recording
 13952-13954  _prune_stall_dumps
 12318-12439  _public_stats
 19203-19229  _push_notify
 10379-10381  _pwa_dir
 11460-11475  _quick_validate_proxy
 14498-14500  _quiet_hours_config
 10344-10377  _rate_guard
 18494-18500  _react_warn
  7644-7683   _reap_proc
  2390-2412   _record_check_outcome
   726-728    _redact_stream_urls
 11643-11713  _refresh_proxy_pool
 21884-21890  _resolve_piper_model
  2184-2274   _resolve_via_html
  2532-2686   _resolve_via_webcast_api_v2
  2749-2811   _resolve_via_ytdlp
 26413-26542  _resolve_youtube_ingest
 20135-20142  _restream_active_platforms
 15009-15020  _restream_active_sources
 19713-19812  _restream_chat_guardian
 15174-15246  _restream_chat_push
 14936-14948  _restream_enabled
 15615-15702  _restream_html_overlay_start
 15705-15718  _restream_html_overlay_stop
  1126-1128   _restream_layout_mode
 14974-14997  _restream_overlay_files
 20100-20132  _restream_platform_state
 20263-20298  _restream_resume_after_restart
 15766-15824  _restream_tts_enqueue_wav
 15489-15521  _restream_tts_feeder
 15486-15487  _restream_tts_fifo_path
 15721-15748  _restream_tts_start
 15750-15764  _restream_tts_stop
 20145-20260  _restream_verify_loop
 25427-25439  _retention_loop
 25386-25424  _retention_scan
  2494-2496   _room_is_abo
  5992-6109   _run_ai_call
 14090-14103  _run_async_from_flask
 22646-22649  _run_priv
 29157-29165  _run_selfcheck_and_exit
 25442-25453  _s3_client
  7924-7975   _safe_send
  4587-4603   _sample_net_throughput
 17520-17528  _save_banned_words_file
  2442-2469   _schedule_next_check
 25340-25383  _scheduler_loop
  3909-3913   _schema_pk
 14107-14112  _scraper_session
 27091-27130  _screen_full
 12910-12947  _sec_headers
  2163-2165   _select_stream_from_data_section
 28970-29154  _selfcheck
  8698-8732   _send_live_notice
  1201-1205   _should_defer_upload
 25855-25890  _shrink_for_discord
 10384-10396  _sicheres_ziel
 28362-28379  _sign_health_check
 28382-28401  _sign_health_loop
  7753-7764   _spawn
  7767-7797   _spawn_from_flask
 22969-22972  _st_befund
 19438-19679  _start_chat_listener
 14070-14087  _start_loop_watchdog
 12463-12491  _stats_loop
 12442-12445  _stats_output_path
 12448-12460  _stats_write
  8426-8442   _storage_cleanup_loop
 28421-28428  _story_for
  3201-3207   _stream_url_expiry
  3216-3222   _stream_url_is_fresh
  3209-3214   _stream_url_ttl
 17593-17600  _streamer_persona_get
 17575-17581  _streamer_personas_load
 17572-17573  _streamer_personas_path
 17583-17591  _streamer_personas_save
 15441-15445  _studio_chain
 25559-25681  _system_backup
 25684-25714  _system_backup_loop
 11412-11451  _test_proxy
 12118-12127  _testpush_cfg
 12130-12147  _testpush_exec
 12099-12115  _testpush_resolve_live
  7900-7921   _tg_sprache_setzen
  8605-8615   _tg_topics_load_into_mem
  8602-8603   _tg_topics_path
  8617-8624   _tg_topics_save
 10192-10200  _token_ok
  8627-8631   _topic_forget
 14518-14529  _tracking_max_duration
  4174-4188   _tracking_remove_cleanup
  4205-4217   _tracking_resume_cleanup
  1435-1458   _try_attach_file_handler
 21928-21936  _tts_cleanup
 12055-12059  _tunnel_effective
 21354-21407  _twitch_channel_status
 27133-27276  _twitch_chat_loop
 26947-27050  _twitch_eventsub_loop
  1224-1237   _upload_queue_add
  1248-1250   _upload_queue_count
  1207-1216   _upload_queue_load
  1197-1199   _upload_queue_path
  1239-1246   _upload_queue_remove
  1218-1222   _upload_queue_save
  1252-1293   _upload_window_loop
  7617-7624   _uptime_s
 14951-14960  _url_host
   706-723    _url_ohne_zugang
   790-794    _usage_record_claude
  7838-7882   _verbindung_verloren
  6721-6752   _viewer_sample_loop
  6794-6801   _viewer_stats
 10281-10284  _wants_html
  7627-7641   _warn_empty_env
 28177-28272  _watchdog_loop
 26688-26696  _wchat_thank_ok
 19272-19302  _whisper_get_model
  7714-7721   _whisper_native_section
 18481-18487  _whisper_pool
 19371-19400  _whisper_segments
 19304-19368  _whisper_transcribe
 15272-15434  _write_restream_overlay
 27304-27383  _youtube_api_chat_loop
 21410-21513  _youtube_api_status
 21516-21583  _youtube_channel_status
 27386-27546  _youtube_chat_loop
 26548-26561  _youtube_restream_autoconfig
 26564-26588  _youtube_restream_autoconfig_inner
 26655-26683  _youtube_send
 21688-21729  _youtube_set_channel
 26591-26625  _yt_access_token
 26628-26643  _yt_live_chat_id
 27297-27301  _yt_oauth_configured
 26651-26652  _yt_sendrate_cfg
 27279-27294  _yt_timeout
  2733-2734   _ytdlp_detect_available
  2736-2747   _ytdlp_note_result
 13957-13959  _zombie_child_count
  7494-7518   about
  4084-4088   add_ai_log_entry
  4001-4004   add_archive_entry
  4700-4715   add_archive_rule
  4376-4410   add_recording
  4149-4166   add_tracking
  6112-6145   ai
  3748-3787   ai_chat
  3821-3831   ai_history_append
  3833-3838   ai_history_clear
  3810-3819   ai_history_load
  3795-3808   ai_rate_limit_check
  6174-6182   aireset
 18812-18831  azrael_chat
 27551-27673  brain_cmd
  3225-3409   build_recording_cmd
  4169-4172   bulk_add_trackings
  6991-7050   bulkadd
  8445-8585   check_all_trackings
  4221-4233   claim_live_transition
 17669-18424  class KickModerator
 16037-17353  class RestreamManager
 11829-11871  classify_proxy_anonymity
  6220-6418   cleanup
  5183-5224   cleanup_old_recordings
  4367-4374   clear_recording
 26300-26365  clip_moment
  4531-4580   compute_storage_forecast
  7113-7157   cookies_cmd
  4140-4146   count_trackings_for_chat
  4071-4082   decide_preferred_recorder
  4011-4014   delete_archive_entry
  4717-4725   delete_archive_rule
  5649-5796   diag
 27785-27846  einnahmen_cmd
  4525-4528   find_recordings_by_fingerprint
  4032-4048   finish_recording_attempt
  4193-4195   get_all_active_trackings
  4099-4102   get_all_checks
  4412-4415   get_all_recordings
  4474-4476   get_all_tags_with_counts
  4502-4505   get_annotations_for_recording
  4006-4009   get_archive_entry
  4495-4498   get_bookmarked_recordings
  1912-2029   get_cookie_health
  4462-4468   get_event_log
  4055-4069   get_last_recording_attempt
  2814-2919   get_live_status
  4983-4986   get_manual_recordings
  4510-4513   get_or_compute_inspect_sync
  5259-5303   get_outcome_breakdown
  4481-4484   get_priority_poll_interval
  4678-4687   get_profile_snapshots
  4050-4053   get_recent_recording_attempts
  4417-4420   get_recording_by_id
  4488-4491   get_recording_note
  3543-3566   get_redis
  4129-4132   get_stats
  5150-5181   get_storage_stats
  4818-4820   get_tiktok_status_distribution
  4235-4244   get_tracking_state
  4190-4191   get_trackings_for_group
  4999-5002   get_trash_recordings
  9353-10016  handle_recording_finished
  3931-3956   init_db
  5073-5127   inspect_stream_url
 22047-22049  is_revenue_platform
  4690-4698   list_archive_rules
  5453-5491   live
  7978-7986   live_check_worker
  3618-3652   llm_chat
  3675-3703   llm_chat_sync
  3660-3672   llm_list_models
  4428-4454   log_event
  1503-1536   log_recording_failure
  7307-7356   logs_cmd
 28469-28960  main
  6148-6171   on_ai_media
  7433-7459   on_ai_reply
  7462-7491   on_azrael_mention
  7523-7553   on_callback
 18834-18938  oracle_handle
  7196-7199   pause_tracking
  5313-5318   profile_keyboard
  7258-7304   quota
  8356-8423   reaper_loop
  4814-4816   record_tiktok_status
  6187-6217   recstatus
  3568-3576   redis_get_json
  3578-3584   redis_set_json
 27849-27859  report_cmd
 11874-11876  report_proxy_result
  2277-2304   resolve_tiktok_live_stream
  4994-4997   restore_recording
  7202-7205   resume_tracking
  4728-4808   run_archive_rules
 27862-28084  run_bot
 13879-13926  run_flask
  4606-4651   sample_bandwidth_for_active
  4657-4676   save_profile_snapshot
  4091-4097   save_tiktok_check
  4359-4365   set_recording_file
  4198-4202   set_tracking_paused
  4989-4992   soft_delete_recording
  8738-9351   split_and_send_video
  5366-5408   start
  4016-4030   start_recording_attempt
  6421-6459   stats
  4964-4981   stop_manual_recording
  7208-7255   stoprec
  6646-6654   summary_cmd
  7359-7430   sysres
  5798-5942   teststream
  5410-5451   tiktok
  7053-7110   topusers
  5528-5585   track
  5493-5525   track_exact
  5599-5647   tracklist
  4830-4962   trigger_manual_recording
  4320-4357   try_acquire_recording_lock
  5005-5064   universal_search
  5587-5597   untrack
 27676-27782  update_cmd
  4520-4523   update_recording_fingerprint
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
restream_util.py       looks_like_source_expired, normalize_ingest
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
util.py                —
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
