# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (143)

```
 10471  GET              /                                                dashboard
 13936  GET              /api/abo/status                                  api_abo_status
 10544  GET              /api/active-recordings                           api_active_recordings
 14007  GET              /api/activity-pulse                              api_activity_pulse
 13814  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 20484  GET/POST         /api/audio/config                                api_audio_config
 20514  POST             /api/audio/testtone                              api_audio_testtone
 13880  GET/POST         /api/auto-archive-rules                          api_archive_rules
 13904  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete
 13908  POST             /api/auto-archive-rules/run                      api_archive_rules_run
 11998  GET              /api/automation/status                           api_automation_status
 12020  POST             /api/automation/toggle                           api_automation_toggle
 12942  GET              /api/azrael/agents                               api_azrael_agents
 11890  POST             /api/azrael/ask                                  api_azrael_ask
 20682  GET/POST         /api/azrael/context                              api_azrael_context
 12740  GET              /api/azrael/core                                 api_azrael_core
 20833  POST             /api/azrael/live_pause                           api_azrael_live_pause
 20823  GET              /api/azrael/live_status                          api_azrael_live_status
 20841  POST             /api/azrael/live_test                            api_azrael_live_test
 12951  GET              /api/azrael/memories                             api_azrael_memories
 20889  POST             /api/azrael/persona                              api_azrael_persona_set
 20880  GET              /api/azrael/personas                             api_azrael_personas
 20917  GET              /api/azrael/piper_status                         api_azrael_piper_status
 20655  POST             /api/azrael/react                                api_azrael_react
 20691  GET              /api/azrael/reaction                             api_azrael_reaction
 20860  GET              /api/azrael/reactions                            api_azrael_reactions
 20910  GET              /api/azrael/transcript                           api_azrael_transcript
 20795  POST             /api/azrael/tts_test                             api_azrael_tts_test
 20766  GET              /api/azrael/voices                               api_azrael_voices
 20934  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model
 10843  GET              /api/backoff-watch                               api_backoff_watch
 13376  POST             /api/backup/run                                  api_backup_run
 13342  GET              /api/backup/status                               api_backup_status
 13331  POST             /api/backup/system                               api_backup_system
 13846  GET              /api/bandwidth/live                              api_bandwidth_live
 13799  GET              /api/bookmarks                                   api_bookmarks_list
 11106  GET              /api/brain                                       api_brain
 11043  GET              /api/brain/alarms                                api_brain_alarms
 11028  GET              /api/brain/creator                               api_brain_creator
 11005  GET              /api/brain/graph                                 api_brain_graph
 11066  GET              /api/brain/growth                                api_brain_growth
 10021  GET              /api/brain/health                                api_brain_health
 21378  GET              /api/channel/categories                          api_channel_categories
 21384  POST             /api/channel/set                                 api_channel_set
 21231  GET              /api/channels/status                             api_channels_status
 10525  GET              /api/checks                                      api_checks
 20719  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 20702  GET              /api/clips                                       api_clips
 20748  POST/DELETE      /api/clips/clear                                 api_clips_clear
 14315  GET              /api/community/stats                             api_community_stats
 22018  GET              /api/data/export                                 api_data_export
 20377  GET              /api/debug/threads                               api_debug_threads
 22865  GET              /api/defense/attacks                             api_defense_attacks
 22832  GET              /api/defense/crowdsec                            api_defense_crowdsec
 22850  GET              /api/defense/fail2ban                            api_defense_fail2ban
 22556  GET              /api/defense/overview                            api_defense_overview
 13828  GET              /api/events                                      api_events
 13213  GET              /api/events/stream                               api_events_stream
 13841  GET              /api/forecast/storage                            api_forecast_storage
 12036  GET              /api/freeai/status                               api_freeai_status
 12783  GET              /api/health                                      api_health
 13859  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 13855  GET              /api/heatmap/recordings                          api_heatmap_recordings
 20455  GET              /api/highlights                                  api_highlights
 20467  POST             /api/highlights/config                           api_highlights_config
 20563  POST             /api/kickmod/config                              api_kickmod_config
 20608  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords
 20622  GET              /api/kickmod/learned                             api_kickmod_learned
 20649  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear
 20629  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote
 20977  POST             /api/kickmod/say                                 api_kickmod_say
 20953  POST             /api/kickmod/start                               api_kickmod_start
 20534  GET              /api/kickmod/status                              api_kickmod_status
 20964  POST             /api/kickmod/stop                                api_kickmod_stop
 10405  POST             /api/login                                       dashboard_login_submit
 14300  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 14269  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 13111  GET              /api/notify/status                               api_notify_status
 13122  POST             /api/notify/test                                 api_notify_test
 10629  GET              /api/outcomes                                    api_outcomes
 21855  POST             /api/overlay/config                              api_overlay_config
 21842  POST             /api/overlay/event                               api_overlay_event
 21747  GET              /api/overlay/state                               api_overlay_state
 10662  GET              /api/profile/<username>                          api_profile
 14025  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk
 13867  GET              /api/profile/snapshots/<username>                api_profile_snapshots
 13990  GET              /api/proxy/heatmap                               api_proxy_heatmap
 13967  GET              /api/proxy/trend                                 api_proxy_trend
 12491  GET              /api/public/stats                                api_public_stats
 10505  GET              /api/pulse                                       api_pulse
 13435  GET              /api/recording-attempts                          api_recording_attempts
 20179  POST             /api/restream/<int:rid>/delete                   api_restream_delete
 20157  POST             /api/restream/<int:rid>/edit                     api_restream_edit
 20198  POST             /api/restream/<int:rid>/start                    api_restream_start
 20398  POST             /api/restream/<int:rid>/stop                     api_restream_stop
 21709  GET              /api/restream/chatfeed                           api_restream_chatfeed
 20133  POST             /api/restream/create                             api_restream_create
 12616  GET              /api/restream/deck                               api_restream_deck
 11972  GET              /api/restream/health                             api_restream_health
 21731  POST             /api/restream/layout                             api_restream_layout
 20106  GET              /api/restream/list                               api_restream_list
 11941  POST             /api/restream/report                             api_restream_report
 20411  POST             /api/restream/start_all                          api_restream_start_all
 20437  POST             /api/restream/stop_all                           api_restream_stop_all
 12147  GET              /api/restream/testpush                           api_testpush_status
 12172  POST             /api/restream/testpush                           api_testpush_run
 14400  GET              /api/restream/verify                             api_restream_verify
 13160  GET              /api/retention/preview                           api_retention_preview
 13169  POST             /api/retention/run                               api_retention_run
 13784  GET              /api/search                                      api_search
 22603  GET              /api/selftest                                    api_selftest
 20215  GET              /api/shield/stats                                api_shield_stats
 10566  GET              /api/storage                                     api_storage
 10573  POST             /api/storage/cleanup                             api_storage_cleanup
 13921  GET              /api/stream/inspect/<username>                   api_stream_inspect
 11911  GET              /api/stream/timeline                             api_stream_timeline
 12844  GET              /api/stream/transcript                           api_stream_transcript
 10597  GET              /api/summary/preview                             api_summary_preview
 13500  GET              /api/system                                      api_system
 14348  GET              /api/system/check_timing                         api_check_timing
 14463  GET              /api/system/config_drift                         api_config_drift
 12858  GET              /api/system/config_snapshot                      api_system_config_snapshot
 12969  GET              /api/system/preflight                            api_system_preflight
 13095  GET              /api/system/preflight_history                    api_system_preflight_history
 13278  GET              /api/system/resilience                           api_system_resilience
 13819  GET              /api/tags                                        api_tags_list
 10539  GET              /api/top                                         api_top
 10898  GET              /api/trend-7d                                    api_trend_7d
 20780  GET              /api/tts/<fn>                                    api_tts_file
 21883  GET              /api/upload_window                               api_upload_window
 10643  GET              /api/userstats                                   api_userstats
 12539  GET              /api/version                                     api_version
 13473  GET              /archive/<int:eid>/download                      archive_download
 13530  GET              /download/<int:recording_id>                     download
 13413  GET              /health                                          health
 20346  GET              /healthz                                         healthz
 10396  GET              /login                                           dashboard_login_page
 10426  GET              /logout                                          dashboard_logout
 10433  GET              /manifest.webmanifest                            pwa_manifest
 12886  GET              /metrics                                         api_prometheus_metrics
 21692  GET              /overlay                                         overlay_page
 10457  GET              /pwa-icon-<variant>.png                          pwa_icon
 10443  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (216)

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
   227  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   153  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   171  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   143  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    46  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   119  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
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
 23329  /ai                     
 23788  /ask                    
 23420  /assign_role            
 23466  /ban                    
 24120  /botstats               
 24044  /clearwarns             
 24084  /clip                   
 24069  /clipoftheweek          
 23911  /clips                  
 23381  /create_category        
 23350  /create_channel         
 23409  /create_group           
 23392  /create_role            
 23366  /create_voice           
 23702  /daily                  
 23818  /event                  
 23861  /events                 
 23957  /follow                 
 23941  /help                   
 23455  /kick                   
 23684  /leaderboard            
 23897  /livenow                
 23927  /post_test              
 23758  /profile                
 23490  /purge                  
 23670  /rank                   
 23884  /recstatus              
 23431  /remove_role            
 23343  /restream_status        
 23442  /set_channel_perms      
 23635  /setup_community        
 23653  /setup_targets          
 23983  /stats                  
 23255  /status                 
 24279  /streaminfo             
 24176  /sys_report             
 24152  /sys_unpause            
 23477  /timeout                
 24055  /topstreamers           
 23285  /track                  
 23269  /tracklist              
 23972  /unfollow               
 23318  /untrack                
 24005  /warn                   
 24029  /warnings               
```

## Discord-Events (4)

```
 24763  on_member_join
 24725  on_message
 24366  on_raw_reaction_add
 24798  on_ready
```

## Top-Level-Symbole in bot.py (510 Funktionen, 2 Klassen)

```
  2500-2501   _abo_key
  2521-2539   _abo_probe_dump
 22125-22135  _active_recorder_sync
 17395-17402  _ad_allowlist
 18522-18528  _agent_for
 22137-22155  _ai_calls_total_sync
 18531-18547  _ai_telemetry
 19029-19047  _alert
 24914-24964  _alert_monitor_loop
 25345-25407  _announce_loop
  3442-3445   _anthropic_key
  3452-3454   _anthropic_model
 10149-10152  _arg_int
  2492-2497   _as_dict
 15144-15149  _audio_cfg
 19183-19205  _audio_tap_cmd
 10317-10328  _auth_cookie
 10284-10313  _auth_guard
  1648-1653   _auto_on
 20082-20100  _auto_restream_loop
 26463-26478  _azrael_broadcast_reply
 26363-26385  _azrael_chat_reply
 26346-26360  _azrael_chat_should_reply
 26391-26393  _azrael_gate_cfg
 18552-18566  _azrael_live_state
 21595-21609  _azrael_overlay_state
 18912-18966  _azrael_proactive_loop
 18371-18427  _azrael_reaction_to_chats
 26396-26403  _azrael_reply_all_chats
 26333-26343  _azrael_self_names
 26431-26460  _azrael_send_to
 18569-18590  _azrael_system
 25083-25086  _backup_active
 25164-25177  _backup_loop
 17283-17284  _badwords_path
 24876-24885  _brain_growth_loop
 10974-11001  _brain_growth_snapshot
  2428-2448   _brain_hint_delay
 10966-10968  _brain_history_for
  6533-6561   _brain_notify
 10943-10964  _brain_record
 10970-10972  _brain_stream_recent
 13192-13209  _browser_push
  6577-6664   _build_daily_summary
  2931-3111   _build_native_cmd
 15505-15692  _build_restream_cmd
  3155-3188   _build_ytdlp_cmd
 22077-22084  _cached_probe
  5355-5382   _can_stop_tracking
  1828-1850   _capture_set_cookies
 14084-14087  _cfg_get
 14090-14092  _cfg_set
 21339-21374  _channel_set_all
 14742-14745  _chat_connected
 14748-14764  _chat_disconnected
  8629-8640   _chat_is_forum
 14784-14786  _chat_sanitize
 14788-14797  _chat_src_ok
 14727-14739  _chat_stat
 14767-14770  _chat_stats_snapshot
  3717-3728   _check_ai_alive_sync
  3731-3743   _check_ai_models_sync
 22086-22099  _check_redis_alive_sync
 22101-22121  _check_redis_version_sync
 11573-11616  _classify_pool_anonymity
 11619-11636  _classify_pool_anonymity_bg
   806-810    _claude_chat_sync_metered
 10178-10185  _client_ip
 25439-25466  _clip_prune
 25469-25479  _clip_recfile_for
 25992-25998  _clip_should_velocity
 25520-25602  _clip_to_discord
  3615-3624   _close_ai_session
 26509-26524  _cohost_broadcast
 26494-26495  _cohost_cfg
 26550-26562  _cohost_fire_highlight
 26498-26506  _cohost_gate
 26527-26547  _cohost_highlight
 25651-25685  _community_events_loop
 10797-10799  _conv_messages
  6941-6984   _cookie_alarm_loop
  1900-1904   _cookie_autorefresh_info
  1805-1809   _cookie_header
 13242-13274  _cpu_load_snapshot
  3937-3949   _create_index_safe
 22358-22464  _crowdsec_status
 22304-22355  _crowdsec_via_lapi
 22169-22187  _cscli_bin
 22193-22206  _cscli_path
  6831-6856   _daily_summary_loop
 22224-22241  _darf_journal_lesen
 24888-24911  _db_maintenance_loop
  6800-6828   _db_vacuum_loop
 17418-17442  _detect_foreign_ad
  1386-1397   _diag_path_owner
 18818-18862  _director_finalize
 19629-19636  _director_for
 18767-18815  _director_mark
 25886-25921  _disc_automod_check
 25862-25865  _disc_state_get
 25868-25875  _disc_state_set
 22907-22920  _discord_guild_filesize_bytes
 23112-23116  _discord_invite
 25823-25859  _discord_live_thread
 18969-18981  _discord_notify
 23011-23036  _discord_ops_alert
 25721-25819  _discord_post_user
 23172-24873  _discord_run_once
 23051-23109  _discord_start
 25410-25416  _discord_stop
 22928-22930  _discord_upload_limit_label
 22923-22925  _discord_upload_limit_mb
  6859-6936   _disk_alarm_loop
 27942-27991  _disk_autoclean
 27994-28007  _disk_guard_loop
 27934-27939  _disk_pct
 15101-15103  _drawtext_chain
 13627-13629  _dump_all_threads
 11498-11562  _enrich_proxies_with_geo
  2045-2089   _ensure_cookie_file_netscape
 23119-23169  _ensure_discord_invite
 25616-25648  _ensure_error_channel
  8688-8691   _ensure_notify_topic
 11743-11780  _ensure_proxy_ready
  8642-8669   _ensure_topic
   663-665    _env_int
   668-670    _env_int_range
 25688-25718  _error_channel_loop
 19013-19026  _event_webhook
 14550-14563  _evolution_loop
  5975-6009   _extract_file_payload
  2177-2179   _extract_urls_from_streamurl_node
 22209-22216  _f2b_sudo_hint
 19049-19051  _faster_whisper_available
 17307-17319  _fetch_ldnoobw_de
 11387-11405  _fetch_proxy_list
 19463-19491  _fetch_tiktok_room_id
   739-742    _ff_cmd
 15264-15269  _find_chromium
  3148-3152   _find_external_recorder
  2182-2184   _find_stream_urls
 14135-14160  _fire_webhooks
  7720-7729   _fork_safe
   821-830    _freeai_chat_sync_metered
 22259-22301  _geo_lookup_ips
  3604-3613   _get_ai_session
  7554-7594   _get_live_info
  2718-2725   _get_resolve_semaphore
  7984-8350   _handle_single_tracking
 27760-27762  _hb
 27765-27782  _hb_while
 14802-14804  _highlight_cfg
 14807-14836  _highlight_observe
 15272-15290  _htmlov_screenshot_cmd
 19207-19217  _httpx_proxy
 14168-14180  _in_quiet_hours
 28821-28852  _install_fast_eventloop
 10044-10098  _install_fast_json
 13632-13648  _install_faulthandler
 20254-20263  _intel_ensure_schema
 20301-20336  _intel_index_loop
 20275-20285  _intel_index_one
 20266-20272  _intel_semantic
  5344-5353   _is_authorized
  7885-7891   _is_dead
  2167-2169   _is_hevc
 22244-22250  _is_private_ip
  1550-1557   _is_process_running
  6563-6574   _is_quiet_hours
  1187-1196   _is_upload_window
 10133-10146  _json_error_handler
  6786-6787   _kick_broadcaster_id
 12073-12092  _kick_channel_live
  6698-6740   _kick_follower_count
  6682-6685   _kick_slug
 12566-12597  _kick_user_token
  3986-3989   _kind_from_filename
 14197-14202  _latest_popularity
 17329-17335  _learned_load
 17326-17327  _learned_path
 17337-17345  _learned_save
 19844-19877  _live_react_loop
 19640-19833  _live_react_worker
 18430-18441  _live_transcript_push
 19835-19842  _live_users
 18865-18909  _living_title_loop
 17286-17294  _load_banned_words_file
  1726-1799   _load_cookies_dict
 25089-25161  _local_backup_scan
 10115-10129  _log_5xx
 15700-15712  _looks_like_codec_err
 15695-15697  _looks_like_source_expired
  7801-7831   _loop_fehler
 13652-13661  _loop_heartbeat
 27730-27757  _loop_lag_monitor
 13664-13732  _loop_watchdog_thread
 18310-18324  _loyalty_add
 18301-18307  _loyalty_get
 18327-18335  _loyalty_top
 14334-14336  _manual_donations_total
  7893-7894   _mark_dead
 12244-12260  _marketing_loop
 26410-26428  _maybe_handle_command
 28093-28117  _maybe_hype_clip
  3904-3927   _migrate_columns
 26689-26700  _mod_is_exempt
 26703-26708  _mod_warn_first
 26711-26714  _mod_warn_text
 14590-14598  _modlog
   940-942    _multistream_targets
  7732-7733   _nc_create_subprocess_exec
  7736-7737   _nc_create_subprocess_shell
 12496-12513  _news_loop
 14628-14630  _normalize_ingest
  2359-2376   _note_check_duration
  8682-8685   _notify_topic_name
 18456-18464  _oracle_memories
 18722-18756  _oracle_memorize
 18467-18480  _oracle_persona
 18449-18453  _oracle_recent_text
 14927-14935  _ov_atomic_write
 14915-14921  _ov_bar
 17242-17254  _ov_clip_text
 14924-14925  _ov_oneline
 21659-21688  _overlay_push
 15218-15261  _overlay_render_size
 14689-14693  _overlay_session_reset
 21611-21614  _overlay_src_ok
 17405-17415  _own_invites
 15213-15215  _parse_size
 22472-22552  _parse_ssh_attacks
  7156-7189   _pause_resume_cmd
  1854-1898   _persist_refreshed_cookies
  1692-1724   _pick_checked_pull_proxy
 10214-10227  _pin_auth_value
 10273-10274  _pin_clear_fail
 10253-10256  _pin_locked
 10259-10270  _pin_note_fail
 10230-10250  _pin_ok
 21501-21503  _piper_available
 21466-21488  _piper_list_voices
 21508-21533  _piper_pick_model
 21545-21592  _piper_say
 21459-21463  _piper_voice_roots
 14097-14132  _post_json_threaded
 15192-15210  _probe_video_size
  1578-1595   _proc_is_recorder
 11485-11496  _proxy_geo_cache_put
 11712-11740  _proxy_pool_refresh_loop
  1658-1689   _proxy_report_recording
 13617-13619  _prune_stall_dumps
 12314-12435  _public_stats
 18984-19010  _push_notify
 10375-10377  _pwa_dir
 11456-11471  _quick_validate_proxy
 14163-14165  _quiet_hours_config
 10340-10373  _rate_guard
 18275-18281  _react_warn
  7640-7679   _reap_proc
  2399-2421   _record_check_outcome
   734-736    _redact_stream_urls
 11639-11709  _refresh_proxy_pool
 21491-21497  _resolve_piper_model
  2193-2283   _resolve_via_html
  2541-2695   _resolve_via_webcast_api_v2
  2758-2820   _resolve_via_ytdlp
 26037-26166  _resolve_youtube_ingest
 19916-19923  _restream_active_platforms
 14674-14685  _restream_active_sources
 19494-19593  _restream_chat_guardian
 14839-14911  _restream_chat_push
 14601-14613  _restream_enabled
 15293-15380  _restream_html_overlay_start
 15383-15396  _restream_html_overlay_stop
  1135-1137   _restream_layout_mode
 14639-14662  _restream_overlay_files
 19881-19913  _restream_platform_state
 20044-20079  _restream_resume_after_restart
 15444-15502  _restream_tts_enqueue_wav
 15154-15186  _restream_tts_feeder
 15151-15152  _restream_tts_fifo_path
 15399-15426  _restream_tts_start
 15428-15442  _restream_tts_stop
 19926-20041  _restream_verify_loop
 25054-25066  _retention_loop
 25013-25051  _retention_scan
  2503-2505   _room_is_abo
  6013-6130   _run_ai_call
 13755-13768  _run_async_from_flask
 22253-22256  _run_priv
 28809-28817  _run_selfcheck_and_exit
 25069-25080  _s3_client
  7920-7971   _safe_send
  4608-4624   _sample_net_throughput
 17296-17304  _save_banned_words_file
  2451-2478   _schedule_next_check
 24967-25010  _scheduler_loop
  3930-3934   _schema_pk
 13772-13777  _scraper_session
 26717-26756  _screen_full
 12799-12836  _sec_headers
  2172-2174   _select_stream_from_data_section
 28622-28806  _selfcheck
  8694-8728   _send_live_notice
  1210-1214   _should_defer_upload
 25482-25517  _shrink_for_discord
 10380-10392  _sicheres_ziel
 28014-28031  _sign_health_check
 28034-28053  _sign_health_loop
  7749-7760   _spawn
  7763-7793   _spawn_from_flask
 22596-22599  _st_befund
 19219-19460  _start_chat_listener
 13735-13752  _start_loop_watchdog
 12459-12487  _stats_loop
 12438-12441  _stats_output_path
 12444-12456  _stats_write
  8422-8438   _storage_cleanup_loop
 28073-28080  _story_for
  3210-3216   _stream_url_expiry
  3225-3231   _stream_url_is_fresh
  3218-3223   _stream_url_ttl
 17369-17376  _streamer_persona_get
 17351-17357  _streamer_personas_load
 17348-17349  _streamer_personas_path
 17359-17367  _streamer_personas_save
 15106-15110  _studio_chain
 25186-25308  _system_backup
 25311-25341  _system_backup_loop
 11408-11447  _test_proxy
 12114-12123  _testpush_cfg
 12126-12143  _testpush_exec
 12095-12111  _testpush_resolve_live
  7896-7917   _tg_sprache_setzen
  8601-8611   _tg_topics_load_into_mem
  8598-8599   _tg_topics_path
  8613-8620   _tg_topics_save
 10188-10196  _token_ok
  8623-8627   _topic_forget
 14183-14194  _tracking_max_duration
  4195-4209   _tracking_remove_cleanup
  4226-4238   _tracking_resume_cleanup
  1444-1467   _try_attach_file_handler
 21535-21543  _tts_cleanup
 12051-12055  _tunnel_effective
 20998-21051  _twitch_channel_status
 26759-26902  _twitch_chat_loop
 26573-26676  _twitch_eventsub_loop
  1233-1246   _upload_queue_add
  1257-1259   _upload_queue_count
  1216-1225   _upload_queue_load
  1206-1208   _upload_queue_path
  1248-1255   _upload_queue_remove
  1227-1231   _upload_queue_save
  1261-1302   _upload_window_loop
  7613-7620   _uptime_s
 14616-14625  _url_host
   714-731    _url_ohne_zugang
   799-803    _usage_record_claude
  7834-7878   _verbindung_verloren
  6743-6774   _viewer_sample_loop
  6790-6797   _viewer_stats
 10277-10280  _wants_html
  7623-7637   _warn_empty_env
 27803-27924  _watchdog_loop
 26312-26320  _wchat_thank_ok
 19053-19083  _whisper_get_model
  7710-7717   _whisper_native_section
 18262-18268  _whisper_pool
 19152-19181  _whisper_segments
 19085-19149  _whisper_transcribe
 14937-15099  _write_restream_overlay
 26930-27009  _youtube_api_chat_loop
 21054-21157  _youtube_api_status
 21160-21227  _youtube_channel_status
 27012-27172  _youtube_chat_loop
 26172-26185  _youtube_restream_autoconfig
 26188-26212  _youtube_restream_autoconfig_inner
 26279-26307  _youtube_send
 21295-21336  _youtube_set_channel
 26215-26249  _yt_access_token
 26252-26267  _yt_live_chat_id
 26923-26927  _yt_oauth_configured
 26275-26276  _yt_sendrate_cfg
 26905-26920  _yt_timeout
  2742-2743   _ytdlp_detect_available
  2745-2756   _ytdlp_note_result
 13622-13624  _zombie_child_count
  7490-7514   about
  4105-4109   add_ai_log_entry
  4022-4025   add_archive_entry
  4721-4736   add_archive_rule
  4397-4431   add_recording
  4170-4187   add_tracking
  6133-6166   ai
  3757-3808   ai_chat
  3842-3852   ai_history_append
  3854-3859   ai_history_clear
  3831-3840   ai_history_load
  3816-3829   ai_rate_limit_check
  6195-6203   aireset
 18593-18612  azrael_chat
 27177-27299  brain_cmd
  3234-3418   build_recording_cmd
  4190-4193   bulk_add_trackings
  6987-7046   bulkadd
  8441-8581   check_all_trackings
  4242-4254   claim_live_transition
 17445-18200  class KickModerator
 15715-17129  class RestreamManager
 11825-11867  classify_proxy_anonymity
  6241-6439   cleanup
  5204-5245   cleanup_old_recordings
  4388-4395   clear_recording
 25924-25989  clip_moment
  4552-4601   compute_storage_forecast
  7109-7153   cookies_cmd
  4161-4167   count_trackings_for_chat
  4092-4103   decide_preferred_recorder
  4032-4035   delete_archive_entry
  4738-4746   delete_archive_rule
  5670-5817   diag
 27411-27472  einnahmen_cmd
  4546-4549   find_recordings_by_fingerprint
  4053-4069   finish_recording_attempt
  4214-4216   get_all_active_trackings
  4120-4123   get_all_checks
  4433-4436   get_all_recordings
  4495-4497   get_all_tags_with_counts
  4523-4526   get_annotations_for_recording
  4027-4030   get_archive_entry
  4516-4519   get_bookmarked_recordings
  1921-2038   get_cookie_health
  4483-4489   get_event_log
  4076-4090   get_last_recording_attempt
  2823-2928   get_live_status
  5004-5007   get_manual_recordings
  4531-4534   get_or_compute_inspect_sync
  5280-5324   get_outcome_breakdown
  4502-4505   get_priority_poll_interval
  4699-4708   get_profile_snapshots
  4071-4074   get_recent_recording_attempts
  4438-4441   get_recording_by_id
  4509-4512   get_recording_note
  3552-3575   get_redis
  4150-4153   get_stats
  5171-5202   get_storage_stats
  4839-4841   get_tiktok_status_distribution
  4256-4265   get_tracking_state
  4211-4212   get_trackings_for_group
  5020-5023   get_trash_recordings
  9349-10012  handle_recording_finished
  3952-3977   init_db
  5094-5148   inspect_stream_url
 21654-21656  is_revenue_platform
  4711-4719   list_archive_rules
  5474-5512   live
  7974-7982   live_check_worker
  3627-3661   llm_chat
  3684-3712   llm_chat_sync
  3669-3681   llm_list_models
  4449-4475   log_event
  1512-1545   log_recording_failure
  7303-7352   logs_cmd
 28121-28612  main
  6169-6192   on_ai_media
  7429-7455   on_ai_reply
  7458-7487   on_azrael_mention
  7519-7549   on_callback
 18615-18719  oracle_handle
  7192-7195   pause_tracking
  5334-5339   profile_keyboard
  7254-7300   quota
  8352-8419   reaper_loop
  4835-4837   record_tiktok_status
  6208-6238   recstatus
  3577-3585   redis_get_json
  3587-3593   redis_set_json
 27475-27485  report_cmd
 11870-11872  report_proxy_result
  2286-2313   resolve_tiktok_live_stream
  5015-5018   restore_recording
  7198-7201   resume_tracking
  4749-4829   run_archive_rules
 27488-27710  run_bot
 13544-13591  run_flask
  4627-4672   sample_bandwidth_for_active
  4678-4697   save_profile_snapshot
  4112-4118   save_tiktok_check
  4380-4386   set_recording_file
  4219-4223   set_tracking_paused
  5010-5013   soft_delete_recording
  8734-9347   split_and_send_video
  5387-5429   start
  4037-4051   start_recording_attempt
  6442-6480   stats
  4985-5002   stop_manual_recording
  7204-7251   stoprec
  6667-6675   summary_cmd
  7355-7426   sysres
  5819-5963   teststream
  5431-5472   tiktok
  7049-7106   topusers
  5549-5606   track
  5514-5546   track_exact
  5620-5668   tracklist
  4851-4983   trigger_manual_recording
  4341-4378   try_acquire_recording_lock
  5026-5085   universal_search
  5608-5618   untrack
 27302-27408  update_cmd
  4541-4544   update_recording_fingerprint
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
discordstate.py        invite, state_get
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
