# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (42)

```
 10055  GET              /                                                dashboard
 12237  GET              /api/abo/status                                  api_abo_status
 12191  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 10843  GET              /api/automation/status                           api_automation_status
 10865  POST             /api/automation/toggle                           api_automation_toggle
 19005  GET              /api/channel/categories                          api_channel_categories
 19011  POST             /api/channel/set                                 api_channel_set
 18858  GET              /api/channels/status                             api_channels_status
 18532  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18515  GET              /api/clips                                       api_clips
 18561  POST/DELETE      /api/clips/clear                                 api_clips_clear
 18440  GET              /api/debug/threads                               api_debug_threads
 12202  GET              /api/events                                      api_events
 11669  GET              /api/events/stream                               api_events_stream
 11335  GET              /api/health                                      api_health
 18474  POST             /api/highlights/config                           api_highlights_config
  9989  POST             /api/login                                       dashboard_login_submit
 12530  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11584  GET              /api/notify/status                               api_notify_status
 11595  POST             /api/notify/test                                 api_notify_test
 12291  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12268  GET              /api/proxy/trend                                 api_proxy_trend
 19933  GET              /api/selftest                                    api_selftest
 11894  GET              /api/system                                      api_system
 12585  GET              /api/system/check_timing                         api_check_timing
 12677  GET              /api/system/config_drift                         api_config_drift
 11400  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11442  GET              /api/system/preflight                            api_system_preflight
 11568  GET              /api/system/preflight_history                    api_system_preflight_history
 11734  GET              /api/system/resilience                           api_system_resilience
 18581  GET              /api/tts/<fn>                                    api_tts_file
 19307  GET              /api/upload_window                               api_upload_window
 11867  GET              /archive/<int:eid>/download                      archive_download
 11924  GET              /download/<int:recording_id>                     download
 11824  GET              /health                                          health
 18409  GET              /healthz                                         healthz
  9980  GET              /login                                           dashboard_login_page
 10010  GET              /logout                                          dashboard_logout
 10017  GET              /manifest.webmanifest                            pwa_manifest
 19280  GET              /overlay                                         overlay_page
 10041  GET              /pwa-icon-<variant>.png                          pwa_icon
 10027  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (317)

```
   172  GET              /api/active-recordings                           api_active_recordings   [nc/routes/auskunft.py]
   379  GET              /api/activity-pulse                              api_activity_pulse   [nc/routes/auskunft.py]
   185  GET              /api/ai-log                                      api_ai_log   [nc/routes/stats.py]
   155  GET              /api/ai-log/<int:entry_id>                       api_ai_log_detail   [nc/routes/stats.py]
   994  GET              /api/ai/anomalies                                api_ai_anomalies   [nc/routes/ai.py]
   734  POST             /api/ai/ask                                      api_ai_ask   [nc/routes/ai.py]
   865  POST             /api/ai/claude/save                              api_claude_save   [nc/routes/ai.py]
   845  GET              /api/ai/claude/status                            api_claude_status   [nc/routes/ai.py]
   883  POST             /api/ai/claude/test                              api_claude_test   [nc/routes/ai.py]
   807  GET              /api/ai/config                                   api_ai_config   [nc/routes/ai.py]
   347  GET              /api/ai/conversations                            api_ai_conversations_list   [nc/routes/ai.py]
   358  POST             /api/ai/conversations                            api_ai_conversations_create   [nc/routes/ai.py]
   368  GET              /api/ai/conversations/<int:conv_id>              api_ai_conversation_get   [nc/routes/ai.py]
   391  DELETE           /api/ai/conversations/<int:conv_id>              api_ai_conversation_delete   [nc/routes/ai.py]
   398  PATCH            /api/ai/conversations/<int:conv_id>              api_ai_conversation_patch   [nc/routes/ai.py]
   409  POST             /api/ai/conversations/<int:conv_id>/messages     api_ai_conversation_send   [nc/routes/ai.py]
   542  POST             /api/ai/conversations/<int:conv_id>/stream       api_ai_conversation_stream   [nc/routes/ai.py]
   640  POST             /api/ai/diagnose                                 api_ai_diagnose   [nc/routes/ai.py]
  1232  GET              /api/ai/forecast-storage                         api_ai_forecast_storage   [nc/routes/ai.py]
  1264  GET              /api/ai/health-score/<username>                  api_ai_health_score   [nc/routes/ai.py]
   331  GET              /api/ai/models                                   api_ai_models   [nc/routes/ai.py]
   947  GET              /api/ai/predict-golive/<username>                api_ai_predict_golive   [nc/routes/ai.py]
   927  POST             /api/ai/query                                    api_ai_query   [nc/routes/ai.py]
  1100  GET              /api/ai/recommendations                          api_ai_recommendations   [nc/routes/ai.py]
  1148  GET              /api/ai/report                                   api_ai_report   [nc/routes/ai.py]
  1199  GET              /api/ai/retry-advice/<username>                  api_ai_retry_advice   [nc/routes/ai.py]
  1058  GET              /api/ai/segments                                 api_ai_segments   [nc/routes/ai.py]
   902  GET              /api/ai/skills                                   api_ai_skills   [nc/routes/ai.py]
   366  GET              /api/archive                                     api_archive   [nc/routes/archive.py]
   630  DELETE           /api/archive/<int:eid>                           api_archive_delete   [nc/routes/archive.py]
   512  POST             /api/archive/<int:eid>/rename                    api_archive_rename   [nc/routes/archive.py]
   495  POST             /api/archive/bulk-delete                         api_archive_bulk_delete   [nc/routes/archive.py]
   487  GET              /api/archive/check                               api_archive_check   [nc/routes/archive.py]
   323  GET              /api/archive/duplicates                          api_archive_duplicates   [nc/routes/archive.py]
   339  POST             /api/archive/duplicates/delete                   api_archive_duplicates_delete   [nc/routes/archive.py]
   674  POST             /api/archive/index/<int:rid>                     api_archive_index_one   [nc/routes/archive.py]
   639  GET              /api/archive/search                              api_archive_search   [nc/routes/archive.py]
   659  GET              /api/archive/status                              api_archive_status   [nc/routes/archive.py]
   546  POST             /api/archive/upload                              api_archive_upload   [nc/routes/archive.py]
    40  GET/POST         /api/audio/config                                api_audio_config   [nc/routes/audio.py]
    69  POST             /api/audio/testtone                              api_audio_testtone   [nc/routes/audio.py]
   216  GET/POST         /api/auto-archive-rules                          api_archive_rules   [nc/routes/wartung.py]
   241  DELETE           /api/auto-archive-rules/<int:rule_id>            api_archive_rule_delete   [nc/routes/wartung.py]
   246  POST             /api/auto-archive-rules/run                      api_archive_rules_run   [nc/routes/wartung.py]
   154  GET              /api/azrael/agents                               api_azrael_agents   [nc/routes/azrael.py]
    90  POST             /api/azrael/ask                                  api_azrael_ask   [nc/routes/azrael.py]
   213  GET/POST         /api/azrael/context                              api_azrael_context   [nc/routes/azrael.py]
   111  GET              /api/azrael/core                                 api_azrael_core   [nc/routes/azrael.py]
   333  POST             /api/azrael/live_pause                           api_azrael_live_pause   [nc/routes/azrael.py]
   319  GET              /api/azrael/live_status                          api_azrael_live_status   [nc/routes/azrael.py]
   341  POST             /api/azrael/live_test                            api_azrael_live_test   [nc/routes/azrael.py]
   165  GET              /api/azrael/memories                             api_azrael_memories   [nc/routes/azrael.py]
   397  POST             /api/azrael/persona                              api_azrael_persona_set   [nc/routes/azrael.py]
   388  GET              /api/azrael/personas                             api_azrael_personas   [nc/routes/azrael.py]
   305  GET              /api/azrael/piper_status                         api_azrael_piper_status   [nc/routes/azrael.py]
   181  POST             /api/azrael/react                                api_azrael_react   [nc/routes/azrael.py]
   222  GET              /api/azrael/reaction                             api_azrael_reaction   [nc/routes/azrael.py]
   234  GET              /api/azrael/reactions                            api_azrael_reactions   [nc/routes/azrael.py]
   363  GET              /api/azrael/transcript                           api_azrael_transcript   [nc/routes/azrael.py]
   272  POST             /api/azrael/tts_test                             api_azrael_tts_test   [nc/routes/azrael.py]
   258  GET              /api/azrael/voices                               api_azrael_voices   [nc/routes/azrael.py]
   370  GET/POST         /api/azrael/whisper_model                        api_azrael_whisper_model   [nc/routes/azrael.py]
   277  GET              /api/backoff-watch                               api_backoff_watch   [nc/routes/beobachtung.py]
   208  POST             /api/backup/run                                  api_backup_run   [nc/routes/wartung.py]
   174  GET              /api/backup/status                               api_backup_status   [nc/routes/wartung.py]
   157  POST             /api/backup/system                               api_backup_system   [nc/routes/wartung.py]
   356  GET              /api/bandwidth/live                              api_bandwidth_live   [nc/routes/auskunft.py]
   333  GET              /api/bookmarks                                   api_bookmarks_list   [nc/routes/auskunft.py]
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
   151  GET              /api/checks                                      api_checks   [nc/routes/auskunft.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   400  GET              /api/community/stats                             api_community_stats   [nc/routes/auskunft.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
   454  GET              /api/data/export                                 api_data_export   [nc/routes/auskunft.py]
   203  GET              /api/db/export                                   api_db_export   [nc/routes/settings.py]
   230  POST             /api/db/import                                   api_db_import   [nc/routes/settings.py]
   190  GET              /api/db/summary                                  api_db_summary   [nc/routes/settings.py]
   155  GET              /api/defense/attacks                             api_defense_attacks   [nc/routes/abwehr.py]
   116  GET              /api/defense/crowdsec                            api_defense_crowdsec   [nc/routes/abwehr.py]
   137  GET              /api/defense/fail2ban                            api_defense_fail2ban   [nc/routes/abwehr.py]
    82  GET              /api/defense/overview                            api_defense_overview   [nc/routes/abwehr.py]
   235  POST             /api/discord/announce                            api_discord_announce   [nc/routes/discord.py]
   161  GET              /api/discord/clips_week                          api_discord_clips_week   [nc/routes/discord.py]
   179  GET              /api/discord/community                           api_discord_community   [nc/routes/discord.py]
   151  GET              /api/discord/invite                              api_discord_invite   [nc/routes/discord.py]
    54  GET              /api/discord/overview                            api_discord_overview   [nc/routes/discord.py]
   127  POST             /api/discord/webhook_test                        api_discord_webhook_test   [nc/routes/discord.py]
    70  POST             /api/donations/add                               api_donations_add   [nc/routes/money.py]
   103  GET              /api/donations/manual                            api_donations_manual   [nc/routes/money.py]
   111  POST             /api/donations/manual/<int:rid>/delete           api_donations_manual_delete   [nc/routes/money.py]
    51  POST             /api/donations/reset                             api_donations_reset   [nc/routes/money.py]
   127  GET              /api/donations/summary                           api_donations_summary   [nc/routes/money.py]
   156  GET              /api/evolution/changelog                         api_evolution_changelog   [nc/routes/evolution.py]
   141  GET              /api/evolution/history                           api_evolution_history   [nc/routes/evolution.py]
    81  GET              /api/evolution/learned                           api_evolution_learned   [nc/routes/evolution.py]
   103  GET              /api/evolution/proposals                         api_evolution_proposals   [nc/routes/evolution.py]
   124  POST             /api/evolution/proposals/<int:pid>/dismiss       api_evolution_dismiss   [nc/routes/evolution.py]
    71  POST             /api/evolution/run                               api_evolution_run   [nc/routes/evolution.py]
   171  GET              /api/evolution/snapshots                         api_evolution_snapshots   [nc/routes/evolution.py]
    35  GET              /api/evolution/status                            api_evolution_status   [nc/routes/evolution.py]
   191  GET              /api/finanzamt/entries                           api_finanzamt_entries   [nc/routes/money.py]
   211  POST             /api/finanzamt/entry                             api_finanzamt_add   [nc/routes/money.py]
   238  GET              /api/finanzamt/export.csv                        api_finanzamt_csv   [nc/routes/money.py]
   351  GET              /api/forecast/storage                            api_forecast_storage   [nc/routes/auskunft.py]
   274  GET              /api/freeai/status                               api_freeai_status   [nc/routes/auskunft.py]
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
   371  GET              /api/heatmap/lives/<username>                    api_heatmap_lives   [nc/routes/auskunft.py]
   366  GET              /api/heatmap/recordings                          api_heatmap_recordings   [nc/routes/auskunft.py]
   442  GET              /api/highlights                                  api_highlights   [nc/routes/auskunft.py]
    64  GET              /api/i18n/katalog                                api_i18n_katalog   [nc/routes/i18n.py]
    53  GET              /api/i18n/sprachen                               api_i18n_sprachen   [nc/routes/i18n.py]
   211  GET              /api/i18n/uebersetzer.js                         api_i18n_js   [nc/routes/i18n.py]
    77  POST             /api/i18n/waehlen                                api_i18n_waehlen   [nc/routes/i18n.py]
   158  GET              /api/insights/activity-clock                     api_insights_activity_clock   [nc/routes/insights.py]
    33  GET              /api/insights/best-times/<username>              api_insights_best_times   [nc/routes/insights.py]
   140  GET              /api/insights/catch-rate                         api_insights_catch_rate   [nc/routes/insights.py]
   115  GET              /api/insights/growth/<username>                  api_insights_growth   [nc/routes/insights.py]
   179  GET              /api/insights/leaderboard                        api_insights_leaderboard   [nc/routes/insights.py]
    66  GET              /api/insights/reliability                        api_insights_reliability   [nc/routes/insights.py]
    89  GET              /api/insights/session-stats                      api_insights_session_stats   [nc/routes/insights.py]
   213  GET              /api/insights/storage-by-streamer                api_insights_storage_by_streamer   [nc/routes/insights.py]
   210  GET              /api/kick/channel                                api_kick_channel   [nc/routes/kick.py]
   232  POST             /api/kick/channel                                api_kick_channel_set   [nc/routes/kick.py]
    91  GET              /api/kick/oauth/callback                         api_kick_oauth_callback   [nc/routes/kick.py]
   159  POST             /api/kick/oauth/disconnect                       api_kick_oauth_disconnect   [nc/routes/kick.py]
   137  POST             /api/kick/oauth/redirect                         api_kick_oauth_redirect   [nc/routes/kick.py]
    76  GET              /api/kick/oauth/start                            api_kick_oauth_start   [nc/routes/kick.py]
   116  GET              /api/kick/oauth/status                           api_kick_oauth_status   [nc/routes/kick.py]
   166  GET/POST         /api/kick/sendcheck                              api_kick_sendcheck   [nc/routes/kick.py]
   110  POST             /api/kickmod/config                              api_kickmod_config   [nc/routes/kickmod.py]
   158  POST             /api/kickmod/import_badwords                     api_kickmod_import_badwords   [nc/routes/kickmod.py]
   175  GET              /api/kickmod/learned                             api_kickmod_learned   [nc/routes/kickmod.py]
   206  POST             /api/kickmod/learned/clear                       api_kickmod_learned_clear   [nc/routes/kickmod.py]
   182  POST             /api/kickmod/learned/promote                     api_kickmod_learned_promote   [nc/routes/kickmod.py]
   242  POST             /api/kickmod/say                                 api_kickmod_say   [nc/routes/kickmod.py]
   212  POST             /api/kickmod/start                               api_kickmod_start   [nc/routes/kickmod.py]
    73  GET              /api/kickmod/status                              api_kickmod_status   [nc/routes/kickmod.py]
   226  POST             /api/kickmod/stop                                api_kickmod_stop   [nc/routes/kickmod.py]
   385  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard   [nc/routes/auskunft.py]
    69  POST             /api/marketing/config                            api_marketing_config   [nc/routes/marketing.py]
    94  GET              /api/marketing/preview                           api_marketing_preview   [nc/routes/marketing.py]
   104  POST             /api/marketing/send-now                          api_marketing_send_now   [nc/routes/marketing.py]
    43  GET              /api/marketing/status                            api_marketing_status   [nc/routes/marketing.py]
    61  POST             /api/marketing/toggle                            api_marketing_toggle   [nc/routes/marketing.py]
   215  GET              /api/moderation/feed                             api_moderation_feed   [nc/routes/stats.py]
    91  POST             /api/news/config                                 api_news_config   [nc/routes/news.py]
    57  GET              /api/news/creators                               api_news_creators   [nc/routes/news.py]
    68  POST             /api/news/creators/generate                      api_news_creators_generate   [nc/routes/news.py]
   133  POST             /api/news/generate-now                           api_news_generate_now   [nc/routes/news.py]
   128  GET              /api/news/items                                  api_news_items   [nc/routes/news.py]
   119  GET              /api/news/preview                                api_news_preview   [nc/routes/news.py]
    44  GET              /api/news/status                                 api_news_status   [nc/routes/news.py]
    83  POST             /api/news/toggle                                 api_news_toggle   [nc/routes/news.py]
   258  GET              /api/ops/audit                                   api_ops_audit   [nc/routes/ops.py]
   325  GET              /api/ops/db-stats                                api_ops_db_stats   [nc/routes/ops.py]
   353  GET              /api/ops/disk-breakdown                          api_ops_disk_breakdown   [nc/routes/ops.py]
   204  GET              /api/ops/errors                                  api_ops_errors   [nc/routes/ops.py]
   271  GET              /api/ops/healthcheck                             api_ops_healthcheck   [nc/routes/ops.py]
   506  GET              /api/ops/log-tail                                api_ops_log_tail   [nc/routes/ops.py]
    71  GET              /api/ops/logtail                                 api_ops_logtail   [nc/routes/ops.py]
   169  GET              /api/ops/metrics                                 api_ops_metrics   [nc/routes/ops.py]
   152  GET              /api/ops/resource_history                        api_ops_resource_history   [nc/routes/ops.py]
   392  GET              /api/ops/version                                 api_ops_version   [nc/routes/ops.py]
   215  GET              /api/outcomes                                    api_outcomes   [nc/routes/auskunft.py]
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   168  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   451  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   426  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   286  GET              /api/public/stats                                api_public_stats   [nc/routes/auskunft.py]
   132  GET              /api/pulse                                       api_pulse   [nc/routes/auskunft.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
   304  GET              /api/recording-attempts                          api_recording_attempts   [nc/routes/auskunft.py]
   485  GET/POST         /api/recordings/<int:rid>/annotations            api_recording_annotations   [nc/routes/recordings.py]
   480  POST             /api/recordings/<int:rid>/bookmark               api_recording_bookmark   [nc/routes/recordings.py]
   528  POST             /api/recordings/<int:rid>/fingerprint            api_recording_fingerprint   [nc/routes/recordings.py]
   411  GET              /api/recordings/<int:rid>/inspect                api_recording_inspect   [nc/routes/recordings.py]
   738  POST             /api/recordings/<int:rid>/label                  api_recording_label   [nc/routes/recordings.py]
   502  GET              /api/recordings/<int:rid>/manifest               api_recording_manifest   [nc/routes/recordings.py]
   465  GET/POST/DELETE  /api/recordings/<int:rid>/notes                  api_recording_notes   [nc/routes/recordings.py]
   438  GET              /api/recordings/<int:rid>/quality                api_recording_quality   [nc/routes/recordings.py]
   712  POST             /api/recordings/<int:rid>/rating                 api_recording_rating   [nc/routes/recordings.py]
   582  POST             /api/recordings/<int:rid>/restore                api_recording_restore   [nc/routes/recordings.py]
   671  POST             /api/recordings/<int:rid>/star                   api_recording_star   [nc/routes/recordings.py]
   577  POST             /api/recordings/<int:rid>/trash                  api_recording_trash   [nc/routes/recordings.py]
   510  GET              /api/recordings/<int:rid>/waveform               api_recording_waveform   [nc/routes/recordings.py]
   290  POST             /api/recordings/<int:tracking_id>/stop           api_recording_stop   [nc/routes/recordings.py]
   755  GET              /api/recordings/by-label/<label>                 api_recordings_by_label   [nc/routes/recordings.py]
   378  GET              /api/recordings/daily                            api_recordings_daily   [nc/routes/recordings.py]
   633  POST             /api/recordings/dedup-scan                       api_dedup_scan   [nc/routes/recordings.py]
   788  GET              /api/recordings/disconnects                      api_recording_disconnects   [nc/routes/recordings.py]
   773  GET              /api/recordings/labels                           api_recordings_labels   [nc/routes/recordings.py]
   334  GET              /api/recordings/list                             api_recordings_list   [nc/routes/recordings.py]
   572  POST             /api/recordings/manual/<int:mid>/stop            api_manual_stop   [nc/routes/recordings.py]
   558  GET              /api/recordings/manual/list                      api_manual_list   [nc/routes/recordings.py]
   541  POST             /api/recordings/manual/start                     api_manual_start   [nc/routes/recordings.py]
   598  GET              /api/recordings/overview                         api_recordings_overview   [nc/routes/recordings.py]
   691  GET              /api/recordings/starred                          api_recordings_starred   [nc/routes/recordings.py]
   587  GET              /api/recordings/trash                            api_trash_list   [nc/routes/recordings.py]
   477  POST             /api/restream/<int:rid>/delete                   api_restream_delete   [nc/routes/restream.py]
   455  POST             /api/restream/<int:rid>/edit                     api_restream_edit   [nc/routes/restream.py]
   496  POST             /api/restream/<int:rid>/start                    api_restream_start   [nc/routes/restream.py]
   513  POST             /api/restream/<int:rid>/stop                     api_restream_stop   [nc/routes/restream.py]
   565  GET              /api/restream/chatfeed                           api_restream_chatfeed   [nc/routes/restream.py]
   431  POST             /api/restream/create                             api_restream_create   [nc/routes/restream.py]
   256  GET              /api/restream/deck                               api_restream_deck   [nc/routes/restream.py]
   156  GET              /api/restream/health                             api_restream_health   [nc/routes/restream.py]
   587  POST             /api/restream/layout                             api_restream_layout   [nc/routes/restream.py]
   404  GET              /api/restream/list                               api_restream_list   [nc/routes/restream.py]
   125  POST             /api/restream/report                             api_restream_report   [nc/routes/restream.py]
   526  POST             /api/restream/start_all                          api_restream_start_all   [nc/routes/restream.py]
   552  POST             /api/restream/stop_all                           api_restream_stop_all   [nc/routes/restream.py]
   182  GET              /api/restream/testpush                           api_testpush_status   [nc/routes/restream.py]
   207  POST             /api/restream/testpush                           api_testpush_run   [nc/routes/restream.py]
   379  GET              /api/restream/verify                             api_restream_verify   [nc/routes/restream.py]
   134  GET              /api/retention/preview                           api_retention_preview   [nc/routes/wartung.py]
   144  POST             /api/retention/run                               api_retention_run   [nc/routes/wartung.py]
   315  POST             /api/schedule/add                                api_schedule_add   [nc/routes/settings.py]
   305  GET              /api/schedule/list                               api_schedule_list   [nc/routes/settings.py]
   340  POST             /api/schedule/remove                             api_schedule_remove   [nc/routes/settings.py]
    56  POST             /api/scheduler/add                               api_scheduler_add   [nc/routes/scheduler.py]
    77  POST             /api/scheduler/delete                            api_scheduler_delete   [nc/routes/scheduler.py]
    43  GET              /api/scheduler/list                              api_scheduler_list   [nc/routes/scheduler.py]
    93  POST             /api/scheduler/toggle                            api_scheduler_toggle   [nc/routes/scheduler.py]
   323  GET              /api/search                                      api_search   [nc/routes/auskunft.py]
   413  GET              /api/shield/stats                                api_shield_stats   [nc/routes/auskunft.py]
   118  GET              /api/stats                                       api_stats   [nc/routes/stats.py]
   209  GET              /api/stats/failures-by-pattern                   api_failures_by_pattern   [nc/routes/stats.py]
   204  GET              /api/stats/tiktok-status                         api_tiktok_status   [nc/routes/stats.py]
   264  GET              /api/stats/timeline                              api_stats_timeline   [nc/routes/stats.py]
   110  GET              /api/storage                                     api_storage   [nc/routes/wartung.py]
   116  POST             /api/storage/cleanup                             api_storage_cleanup   [nc/routes/wartung.py]
   439  GET              /api/stream/inspect/<username>                   api_stream_inspect   [nc/routes/beobachtung.py]
   331  GET              /api/stream/timeline                             api_stream_timeline   [nc/routes/beobachtung.py]
   361  GET              /api/stream/transcript                           api_stream_transcript   [nc/routes/beobachtung.py]
   117  GET              /api/streamer/compare                            api_streamer_compare   [nc/routes/streamer.py]
   264  POST             /api/streamer/delete/<username>                  api_streamer_delete   [nc/routes/streamer.py]
    79  GET              /api/streamer/detail                             api_streamer_detail   [nc/routes/streamer.py]
   289  GET              /api/streamer/digest/<username>                  api_streamer_digest   [nc/routes/streamer.py]
   221  GET              /api/streamer/dormant                            api_streamer_dormant   [nc/routes/streamer.py]
   245  GET              /api/streamer/exists/<username>                  api_streamer_exists   [nc/routes/streamer.py]
   176  GET              /api/streamer/journal/<username>                 api_streamer_journal   [nc/routes/streamer.py]
   141  GET/POST         /api/streamer/priority/<username>                api_streamer_priority   [nc/routes/streamer.py]
   201  GET              /api/streamer/watchlist                          api_streamer_watchlist   [nc/routes/streamer.py]
    47  GET              /api/streamers/wall                              api_streamers_wall   [nc/routes/streamer.py]
   196  GET              /api/summary/preview                             api_summary_preview   [nc/routes/auskunft.py]
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
   346  GET              /api/tags                                        api_tags_list   [nc/routes/auskunft.py]
   166  GET              /api/top                                         api_top   [nc/routes/auskunft.py]
   228  GET              /api/trackings                                   api_trackings   [nc/routes/trackings.py]
   443  POST             /api/trackings/<int:tid>/collection              api_tracking_collection   [nc/routes/trackings.py]
   472  POST             /api/trackings/<int:tid>/max-duration            api_tracking_max_duration   [nc/routes/trackings.py]
   392  GET/POST         /api/trackings/<int:tid>/priority                api_tracking_priority   [nc/routes/trackings.py]
   405  POST             /api/trackings/<int:tid>/quick-restart           api_tracking_quick_restart   [nc/routes/trackings.py]
   501  GET              /api/trackings/<int:tid>/settings                api_tracking_settings   [nc/routes/trackings.py]
   378  GET/POST/DELETE  /api/trackings/<int:tid>/tags                    api_tracking_tags   [nc/routes/trackings.py]
   253  POST             /api/trackings/<int:tracking_id>/notes           api_tracking_notes   [nc/routes/trackings.py]
   298  POST             /api/trackings/<int:tracking_id>/pause           api_tracking_pause   [nc/routes/trackings.py]
   322  POST             /api/trackings/<int:tracking_id>/recheck         api_tracking_recheck   [nc/routes/trackings.py]
   309  POST             /api/trackings/<int:tracking_id>/resume          api_tracking_resume   [nc/routes/trackings.py]
   155  POST             /api/trackings/bulk                              api_trackings_bulk   [nc/routes/trackings.py]
   267  GET              /api/trackings/export                            api_trackings_export   [nc/routes/trackings.py]
   125  GET              /api/trackings/groups                            api_trackings_groups   [nc/routes/trackings.py]
   359  GET              /api/trackings/tags-map                          api_trackings_tags_map   [nc/routes/trackings.py]
   414  GET              /api/trackings/watchlist-export                  api_watchlist_export   [nc/routes/trackings.py]
   242  GET              /api/trend-7d                                    api_trend_7d   [nc/routes/auskunft.py]
   112  POST             /api/tunnel/set                                  api_tunnel_set   [nc/routes/ops.py]
    91  GET              /api/tunnel/status                               api_tunnel_status   [nc/routes/ops.py]
   123  POST             /api/tunnel/test                                 api_tunnel_test   [nc/routes/ops.py]
   104  POST             /api/tunnel/toggle                               api_tunnel_toggle   [nc/routes/ops.py]
   115  GET              /api/twitch/oauth/callback                       api_twitch_oauth_callback   [nc/routes/twitch.py]
    67  POST             /api/twitch/oauth/redirect                       api_twitch_oauth_redirect   [nc/routes/twitch.py]
    91  GET              /api/twitch/oauth/start                          api_twitch_oauth_start   [nc/routes/twitch.py]
    45  GET              /api/twitch/oauth/status                         api_twitch_oauth_status   [nc/routes/twitch.py]
   454  GET              /api/update/backups                              api_update_backups   [nc/routes/ops.py]
   420  GET              /api/update/check                                api_update_check   [nc/routes/ops.py]
   479  POST             /api/update/restart                              api_update_restart   [nc/routes/ops.py]
   459  POST             /api/update/rollback                             api_update_rollback   [nc/routes/ops.py]
   442  POST             /api/update/start                                api_update_start   [nc/routes/ops.py]
   435  GET              /api/update/status                               api_update_status   [nc/routes/ops.py]
   228  GET              /api/userstats                                   api_userstats   [nc/routes/auskunft.py]
   295  GET              /api/version                                     api_version   [nc/routes/auskunft.py]
    42  GET/POST         /api/webhooks                                    api_webhooks   [nc/routes/webhooks.py]
    82  DELETE           /api/webhooks/<int:wid>                          api_webhook_delete   [nc/routes/webhooks.py]
   113  POST             /api/webhooks/<int:wid>/test                     api_webhook_test   [nc/routes/webhooks.py]
    97  POST             /api/webhooks/<int:wid>/toggle                   api_webhook_toggle   [nc/routes/webhooks.py]
   122  GET              /api/youtube/oauth/callback                      api_youtube_oauth_callback   [nc/routes/youtube.py]
   143  POST             /api/youtube/oauth/forget                        api_youtube_oauth_forget   [nc/routes/youtube.py]
   155  POST             /api/youtube/oauth/logout                        api_youtube_oauth_logout   [nc/routes/youtube.py]
    80  POST             /api/youtube/oauth/redirect                      api_youtube_oauth_redirect   [nc/routes/youtube.py]
   104  GET              /api/youtube/oauth/start                         api_youtube_oauth_start   [nc/routes/youtube.py]
    58  GET              /api/youtube/oauth/status                        api_youtube_oauth_status   [nc/routes/youtube.py]
   190  GET              /api/youtube/sendrate                            api_youtube_sendrate   [nc/routes/youtube.py]
   373  GET              /metrics                                         api_prometheus_metrics   [nc/routes/beobachtung.py]
```

## Discord-Slash-Commands (45)

```
 20617  /ai                     
 21076  /ask                    
 20708  /assign_role            
 20754  /ban                    
 21408  /botstats               
 21332  /clearwarns             
 21372  /clip                   
 21357  /clipoftheweek          
 21199  /clips                  
 20669  /create_category        
 20638  /create_channel         
 20697  /create_group           
 20680  /create_role            
 20654  /create_voice           
 20990  /daily                  
 21106  /event                  
 21149  /events                 
 21245  /follow                 
 21229  /help                   
 20743  /kick                   
 20972  /leaderboard            
 21185  /livenow                
 21215  /post_test              
 21046  /profile                
 20778  /purge                  
 20958  /rank                   
 21172  /recstatus              
 20719  /remove_role            
 20631  /restream_status        
 20730  /set_channel_perms      
 20923  /setup_community        
 20941  /setup_targets          
 21271  /stats                  
 20543  /status                 
 21567  /streaminfo             
 21464  /sys_report             
 21440  /sys_unpause            
 20765  /timeout                
 21343  /topstreamers           
 20573  /track                  
 20557  /tracklist              
 21260  /unfollow               
 20606  /untrack                
 21293  /warn                   
 21317  /warnings               
```

## Discord-Events (4)

```
 22053  on_member_join
 22015  on_message
 21654  on_raw_reaction_add
 22088  on_ready
```

## Top-Level-Symbole in bot.py (479 Funktionen, 2 Klassen)

```
  2547-2548   _abo_key
  2568-2586   _abo_probe_dump
 19517-19527  _active_recorder_sync
 15570-15577  _ad_allowlist
 16711-16717  _agent_for
 19529-19547  _ai_calls_total_sync
 16720-16736  _ai_telemetry
 17225-17243  _alert
 22204-22254  _alert_monitor_loop
 22606-22668  _announce_loop
  3489-3492   _anthropic_key
  3499-3501   _anthropic_model
  9733-9736   _arg_int
  2539-2544   _as_dict
 17379-17401  _audio_tap_cmd
  9901-9912   _auth_cookie
  9868-9897   _auth_guard
  1710-1715   _auto_on
 18271-18289  _auto_restream_loop
 23719-23734  _azrael_broadcast_reply
 23619-23641  _azrael_chat_reply
 23602-23616  _azrael_chat_should_reply
 23647-23649  _azrael_gate_cfg
 16741-16755  _azrael_live_state
 19192-19206  _azrael_overlay_state
 17107-17161  _azrael_proactive_loop
 16559-16615  _azrael_reaction_to_chats
 23652-23659  _azrael_reply_all_chats
 23589-23599  _azrael_self_names
 23687-23716  _azrael_send_to
 16761-16782  _azrael_system
 22338-22341  _backup_active
 22419-22432  _backup_loop
 22166-22175  _brain_growth_loop
 10234-10261  _brain_growth_snapshot
  2475-2495   _brain_hint_delay
  6152-6180   _brain_notify
 11648-11665  _browser_push
  6196-6283   _build_daily_summary
  2978-3158   _build_native_cmd
 13756-13943  _build_restream_cmd
  3202-3235   _build_ytdlp_cmd
 19469-19476  _cached_probe
  4974-5001   _can_stop_tracking
  1890-1912   _capture_set_cookies
 12345-12348  _cfg_get
 12351-12353  _cfg_set
 18966-19001  _channel_set_all
 12949-12952  _chat_connected
 12955-12971  _chat_disconnected
  8224-8235   _chat_is_forum
 12991-12993  _chat_sanitize
 12934-12946  _chat_stat
 12974-12977  _chat_stats_snapshot
  3767-3778   _check_ai_alive_sync
  3781-3793   _check_ai_models_sync
 19478-19491  _check_redis_alive_sync
 19493-19513  _check_redis_version_sync
 10516-10559  _classify_pool_anonymity
 10562-10579  _classify_pool_anonymity_bg
   827-849    _claude_chat_sync_metered
  9762-9769   _client_ip
 22700-22727  _clip_prune
 22730-22740  _clip_recfile_for
 23253-23259  _clip_should_velocity
 22781-22863  _clip_to_discord
  3665-3674   _close_ai_session
 23765-23780  _cohost_broadcast
 23750-23751  _cohost_cfg
 23806-23818  _cohost_fire_highlight
 23754-23762  _cohost_gate
 23783-23803  _cohost_highlight
 22912-22946  _community_events_loop
 10164-10166  _conv_messages
  6555-6598   _cookie_alarm_loop
  1962-1966   _cookie_autorefresh_info
  1867-1871   _cookie_header
 11698-11730  _cpu_load_snapshot
  3987-3999   _create_index_safe
 19711-19817  _crowdsec_status
 19657-19708  _crowdsec_via_lapi
 19561-19579  _cscli_bin
 19588-19601  _cscli_path
  6445-6470   _daily_summary_loop
 19619-19636  _darf_journal_lesen
 22178-22201  _db_maintenance_loop
  6414-6442   _db_vacuum_loop
 15593-15617  _detect_foreign_ad
  1445-1456   _diag_path_owner
 17013-17057  _director_finalize
 17825-17832  _director_for
 16962-17010  _director_mark
 23147-23182  _disc_automod_check
 23123-23126  _disc_state_get
 23129-23136  _disc_state_set
 20193-20206  _discord_guild_filesize_bytes
 20400-20404  _discord_invite
 23084-23120  _discord_live_thread
 17164-17176  _discord_notify
 20299-20324  _discord_ops_alert
 22982-23080  _discord_post_user
 20460-22163  _discord_run_once
 20339-20397  _discord_start
 22671-22677  _discord_stop
 20214-20216  _discord_upload_limit_label
 20209-20211  _discord_upload_limit_mb
  6473-6550   _disk_alarm_loop
 25198-25247  _disk_autoclean
 25250-25263  _disk_guard_loop
 25190-25195  _disk_pct
 13349-13351  _drawtext_chain
 12023-12025  _dump_all_threads
 10442-10505  _enrich_proxies_with_geo
  2107-2151   _ensure_cookie_file_netscape
 20407-20457  _ensure_discord_invite
 22877-22909  _ensure_error_channel
  8283-8286   _ensure_notify_topic
 10686-10723  _ensure_proxy_ready
  8237-8264   _ensure_topic
   684-686    _env_int
   689-691    _env_int_range
 22949-22979  _error_channel_loop
 17209-17222  _event_webhook
 12764-12777  _evolution_loop
  5594-5628   _extract_file_payload
  2223-2225   _extract_urls_from_streamurl_node
 19604-19611  _f2b_sudo_hint
 17245-17247  _faster_whisper_available
 10343-10361  _fetch_proxy_list
 17659-17687  _fetch_tiktok_room_id
   760-763    _ff_cmd
 13515-13520  _find_chromium
  3195-3199   _find_external_recorder
  2228-2230   _find_stream_urls
 12396-12421  _fire_webhooks
  7335-7344   _fork_safe
   860-873    _freeai_chat_sync_metered
 19650-19654  _geo_lookup_ips
  3653-3662   _get_ai_session
  7168-7208   _get_live_info
  2765-2772   _get_resolve_semaphore
  7568-7945   _handle_single_tracking
 25016-25018  _hb
 25021-25038  _hb_while
 13005-13007  _highlight_cfg
 13010-13039  _highlight_observe
 13523-13541  _htmlov_screenshot_cmd
 17403-17413  _httpx_proxy
 12429-12441  _in_quiet_hours
 26089-26120  _install_fast_eventloop
  9628-9682   _install_fast_json
 12028-12044  _install_faulthandler
 18317-18326  _intel_ensure_schema
 18364-18399  _intel_index_loop
 18338-18348  _intel_index_one
 18329-18335  _intel_semantic
  4963-4972   _is_authorized
  7469-7475   _is_dead
  2213-2215   _is_hevc
 19639-19641  _is_private_ip
  1609-1616   _is_process_running
  6182-6193   _is_quiet_hours
  1246-1255   _is_upload_window
  9717-9730   _json_error_handler
  6408-6409   _kick_broadcaster_id
  6320-6362   _kick_follower_count
  6304-6307   _kick_slug
 11276-11307  _kick_user_token
  4036-4039   _kind_from_filename
 12458-12463  _latest_popularity
 18040-18073  _live_react_loop
 17836-18029  _live_react_worker
 16618-16629  _live_transcript_push
 18031-18038  _live_users
 17060-17104  _living_title_loop
  1788-1861   _load_cookies_dict
 22344-22416  _local_backup_scan
  9699-9713   _log_5xx
 13951-13963  _looks_like_codec_err
 13946-13948  _looks_like_source_expired
  7385-7415   _loop_fehler
 12048-12057  _loop_heartbeat
 24986-25013  _loop_lag_monitor
 12060-12128  _loop_watchdog_thread
 16498-16512  _loyalty_add
 16489-16495  _loyalty_get
 16515-16523  _loyalty_top
 12571-12573  _manual_donations_total
  7477-7478   _mark_dead
 10962-10978  _marketing_loop
 23666-23684  _maybe_handle_command
 25349-25373  _maybe_hype_clip
  3954-3977   _migrate_columns
 23945-23956  _mod_is_exempt
 23959-23964  _mod_warn_first
 23967-23970  _mod_warn_text
 12804-12812  _modlog
   997-999    _multistream_targets
  7347-7348   _nc_create_subprocess_exec
  7351-7352   _nc_create_subprocess_shell
 11213-11230  _news_loop
 12831-12833  _normalize_ingest
  2406-2423   _note_check_duration
  8277-8280   _notify_topic_name
 16644-16652  _oracle_memories
 16917-16951  _oracle_memorize
 16655-16668  _oracle_persona
 16637-16641  _oracle_recent_text
 13130-13138  _ov_atomic_write
 13118-13124  _ov_bar
 15496-15508  _ov_clip_text
 13127-13128  _ov_oneline
 19244-19273  _overlay_push
 13469-13512  _overlay_render_size
 12897-12901  _overlay_session_reset
 19208-19211  _overlay_src_ok
 15580-15590  _own_invites
 13464-13466  _parse_size
 19825-19905  _parse_ssh_attacks
  6770-6803   _pause_resume_cmd
  1916-1960   _persist_refreshed_cookies
  1754-1786   _pick_checked_pull_proxy
  9798-9811   _pin_auth_value
  9857-9858   _pin_clear_fail
  9837-9840   _pin_locked
  9843-9854   _pin_note_fail
  9814-9834   _pin_ok
 19102-19127  _piper_pick_model
 19139-19186  _piper_say
 12358-12393  _post_json_threaded
 13443-13461  _probe_video_size
  1637-1654   _proc_is_recorder
 10655-10683  _proxy_pool_refresh_loop
  1720-1751   _proxy_report_recording
 12013-12015  _prune_stall_dumps
 11032-11153  _public_stats
 17180-17206  _push_notify
  9959-9961   _pwa_dir
 10412-10427  _quick_validate_proxy
 12424-12426  _quiet_hours_config
  9924-9957   _rate_guard
 16463-16469  _react_warn
  7255-7294   _reap_proc
  2446-2468   _record_check_outcome
   755-757    _redact_stream_urls
 10582-10652  _refresh_proxy_pool
  2239-2329   _resolve_via_html
  2588-2742   _resolve_via_webcast_api_v2
  2805-2867   _resolve_via_ytdlp
 23293-23422  _resolve_youtube_ingest
 12880-12891  _restream_active_sources
 17690-17789  _restream_chat_guardian
 13042-13114  _restream_chat_push
 13544-13631  _restream_html_overlay_start
 13634-13647  _restream_html_overlay_stop
 12842-12865  _restream_overlay_files
 18077-18109  _restream_platform_state
 18233-18268  _restream_resume_after_restart
 13695-13753  _restream_tts_enqueue_wav
 13405-13437  _restream_tts_feeder
 13402-13403  _restream_tts_fifo_path
 13650-13677  _restream_tts_start
 13679-13693  _restream_tts_stop
 18115-18230  _restream_verify_loop
 22309-22321  _retention_loop
 22303-22306  _retention_scan
  2550-2552   _room_is_abo
  5632-5749   _run_ai_call
 12151-12164  _run_async_from_flask
 19644-19647  _run_priv
 26077-26085  _run_selfcheck_and_exit
 22324-22335  _s3_client
  7504-7555   _safe_send
  4611-4627   _sample_net_throughput
  2498-2525   _schedule_next_check
 22257-22300  _scheduler_loop
  3980-3984   _schema_pk
 12168-12173  _scraper_session
 23973-24012  _screen_full
 11351-11388  _sec_headers
  2218-2220   _select_stream_from_data_section
 25890-26074  _selfcheck
  8289-8323   _send_live_notice
  1269-1273   _should_defer_upload
 22743-22778  _shrink_for_discord
  9964-9976   _sicheres_ziel
 25270-25287  _sign_health_check
 25290-25309  _sign_health_loop
  7364-7375   _spawn
 26349-26379  _spawn_from_flask
 19926-19929  _st_befund
 17415-17656  _start_chat_listener
 12131-12148  _start_loop_watchdog
 11180-11208  _stats_loop
 11159-11162  _stats_output_path
 11165-11177  _stats_write
  8017-8033   _storage_cleanup_loop
 25329-25336  _story_for
  3257-3263   _stream_url_expiry
  3272-3278   _stream_url_is_fresh
  3265-3270   _stream_url_ttl
 15543-15550  _streamer_persona_get
 13354-13358  _studio_chain
 22441-22563  _system_backup
 22572-22602  _system_backup_loop
 10364-10403  _test_proxy
 10910-10926  _testpush_resolve_live
  7480-7501   _tg_sprache_setzen
  8196-8206   _tg_topics_load_into_mem
  8193-8194   _tg_topics_path
  8208-8215   _tg_topics_save
  9772-9780   _token_ok
  8218-8222   _topic_forget
 12444-12455  _tracking_max_duration
  4244-4258   _tracking_remove_cleanup
  4275-4287   _tracking_resume_cleanup
  1503-1526   _try_attach_file_handler
 19129-19137  _tts_cleanup
 10886-10890  _tunnel_effective
 18625-18678  _twitch_channel_status
 24015-24160  _twitch_chat_loop
 23829-23932  _twitch_eventsub_loop
  1292-1305   _upload_queue_add
  1316-1318   _upload_queue_count
  1275-1284   _upload_queue_load
  1265-1267   _upload_queue_path
  1307-1314   _upload_queue_remove
  1286-1290   _upload_queue_save
  1320-1361   _upload_window_loop
  7228-7235   _uptime_s
 12819-12828  _url_host
   735-752    _url_ohne_zugang
   820-824    _usage_record_claude
  7418-7462   _verbindung_verloren
  6365-6396   _viewer_sample_loop
  9861-9864   _wants_html
  7238-7252   _warn_empty_env
 25059-25180  _watchdog_loop
 23568-23576  _wchat_thank_ok
 17249-17279  _whisper_get_model
  7325-7332   _whisper_native_section
 16450-16456  _whisper_pool
 17348-17377  _whisper_segments
 17281-17345  _whisper_transcribe
 13185-13347  _write_restream_overlay
 13147-13182  _write_restream_overlay_async
 24184-24264  _youtube_api_chat_loop
 18681-18784  _youtube_api_status
 18787-18854  _youtube_channel_status
 24267-24428  _youtube_chat_loop
 23428-23441  _youtube_restream_autoconfig
 23444-23468  _youtube_restream_autoconfig_inner
 23535-23563  _youtube_send
 18922-18963  _youtube_set_channel
 23471-23505  _yt_access_token
 23508-23523  _yt_live_chat_id
 23531-23532  _yt_sendrate_cfg
 24163-24178  _yt_timeout
  2789-2790   _ytdlp_detect_available
  2792-2803   _ytdlp_note_result
 12018-12020  _zombie_child_count
  7104-7128   about
  4155-4159   add_ai_log_entry
  4072-4075   add_archive_entry
  4649-4651   add_archive_rule
  4446-4480   add_recording
  4219-4236   add_tracking
  5752-5785   ai
  3807-3858   ai_chat
  3892-3902   ai_history_append
  3904-3909   ai_history_clear
  3881-3890   ai_history_load
  3866-3879   ai_rate_limit_check
  5814-5822   aireset
 16785-16804  azrael_chat
 24433-24555  brain_cmd
  3281-3465   build_recording_cmd
  4239-4242   bulk_add_trackings
  6601-6660   bulkadd
  8036-8176   check_all_trackings
  4291-4303   claim_live_transition
 15620-16382  class KickModerator
 13966-15383  class RestreamManager
 10769-10811  classify_proxy_anonymity
  5860-6058   cleanup
  4899-4905   cleanup_old_recordings
  4437-4444   clear_recording
 23185-23250  clip_moment
  4601-4604   compute_storage_forecast
  6723-6767   cookies_cmd
  4210-4216   count_trackings_for_chat
  4142-4153   decide_preferred_recorder
  4082-4085   delete_archive_entry
  4653-4655   delete_archive_rule
  5289-5436   diag
 24667-24728  einnahmen_cmd
  4595-4598   find_recordings_by_fingerprint
  4103-4119   finish_recording_attempt
  4263-4265   get_all_active_trackings
  4170-4172   get_all_checks
  4482-4485   get_all_recordings
  4544-4546   get_all_tags_with_counts
  4572-4575   get_annotations_for_recording
  4077-4080   get_archive_entry
  4565-4568   get_bookmarked_recordings
  1983-2100   get_cookie_health
  4532-4538   get_event_log
  4126-4140   get_last_recording_attempt
  2870-2975   get_live_status
  4838-4841   get_manual_recordings
  4580-4583   get_or_compute_inspect_sync
  4940-4943   get_outcome_breakdown
  4551-4554   get_priority_poll_interval
  4121-4124   get_recent_recording_attempts
  4487-4490   get_recording_by_id
  4558-4561   get_recording_note
  3599-3622   get_redis
  4199-4202   get_stats
  4893-4897   get_storage_stats
  4673-4675   get_tiktok_status_distribution
  4305-4314   get_tracking_state
  4260-4261   get_trackings_for_group
  4854-4857   get_trash_recordings
  8944-9607   handle_recording_finished
  4002-4027   init_db
  4645-4647   list_archive_rules
  5093-5131   live
  7558-7566   live_check_worker
  3677-3711   llm_chat
  3734-3762   llm_chat_sync
  3719-3731   llm_list_models
  4498-4524   log_event
  1571-1604   log_recording_failure
  6917-6966   logs_cmd
 25377-25880  main
  5788-5811   on_ai_media
  7043-7069   on_ai_reply
  7072-7101   on_azrael_mention
  7133-7163   on_callback
 16810-16914  oracle_handle
  6806-6809   pause_tracking
  4953-4958   profile_keyboard
  6868-6914   quota
  7947-8014   reaper_loop
  4669-4671   record_tiktok_status
  5827-5857   recstatus
  3624-3632   redis_get_json
  3635-3641   redis_set_json
 24731-24741  report_cmd
 10814-10816  report_proxy_result
  2332-2359   resolve_tiktok_live_stream
  4849-4852   restore_recording
  6812-6815   resume_tracking
  4658-4663   run_archive_rules
 24744-24966  run_bot
 11938-11985  run_flask
  4633-4636   sample_bandwidth_for_active
  4162-4168   save_tiktok_check
  4429-4435   set_recording_file
  4268-4272   set_tracking_paused
  4844-4847   soft_delete_recording
  8329-8942   split_and_send_video
  5006-5048   start
  4087-4101   start_recording_attempt
  6061-6099   stats
  4819-4836   stop_manual_recording
  6818-6865   stoprec
  6289-6297   summary_cmd
  6969-7040   sysres
  5438-5582   teststream
  5050-5091   tiktok
  6663-6720   topusers
  5168-5225   track
  5133-5165   track_exact
  5239-5287   tracklist
  4685-4817   trigger_manual_recording
  4390-4427   try_acquire_recording_lock
  4860-4862   universal_search
  5227-5237   untrack
 24558-24664  update_cmd
  4590-4593   update_recording_fingerprint
```

## nc/ — öffentliche Symbole

```
__init__.py            —
abo.py                 room_is_abo
admod.py               build_allowlist
aidb.py                add_log_entry, conv_messages
archive.py             add_archive_entry, compute_recording_fingerprint, configure, delete_archive_entry, evaluate_archive_rule, get_archive_entries_paged, get_archive_entry, run_archive_file_check
archivename.py         open_unique
archiverules.py        add_archive_rule, delete_archive_rule, list_archive_rules, run_archive_rules
audio_cue.py           cue_pcm, duck_ratio, mix_chain, silence_pcm, tone_pcm
audiocue.py            config, configure
azraelstate.py         configure, flag, haken, personas_load, personas_path, personas_save
backupcfg.py           aktiv, fehlgrund, lokal, lokal_dir, recordings_retain_days, retention_days, s3, s3_bucket, s3_endpoint, s3_konfiguriert, s3_region, s3_zugang, sys_backup, sys_hour, sys_keep, sys_max_file_mb
badwords.py            banned_path, configure, fetch_ldnoobw_de, learned_path, load_banned, load_learned, save_banned, save_learned
bandbreite.py          messen
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
chatstats.py           summarize
claude.py              api_key, build_payload, chat_sync, fehlertext, is_retired, model, model_raw, parse_response, parse_usage, probe, resolve_model, test_key
cohost.py              config, decide, default_config, new_state, prompt_seed, snapshot
community.py           configure, highlight_post, highlight_share_enabled, live_ping, live_ping_enabled, note_chatter, returning_enabled, seen_stats
confdrift.py           config_drift, extract_defaults, log_watchlist_drift
convmap.py             messages
cookies.py             —
creatoragg.py          summarize
crowdsec.py            base_url, decisions_url, explain_status, headers, parse_decisions
crypto.py              addresses, snapshot
ctx.py                 class Ctx, configure, get, is_configured
dbexport.py            db_export_sql, db_import_sql, export_summary, parse_header
dbwrap.py              configure_db, db_conn, get_pool, set_pool
defensecfg.py          bouncer_gesetzt, bouncer_key, geo_fehler, geo_fehler_setzen, lapi_host, lapi_port, lapi_url, server_lat, server_lon
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
geocache.py            get, groesse, leeren, put
geoip.py               ist_privat, lookup
highlights.py          check, new_state, observe, score, zustand
i18n.py                aktuelle_sprache, aus_accept_language, configure, katalog, normalisieren, sprache_setzen, standard, t
inspectcache.py        parse_row, serialize
journalperm.py         may_read
kick_oauth.py          build_authorize_url, gen_pkce, gen_state, has_scope, is_expired, parse_token_response, token_exchange_payload, token_refresh_payload
kickapi.py             broadcaster_id, configure, oauth_exchange, slug
ledger.py              add_entry, class LedgerError, crosscheck, ensure_schema, entries, export_csv, summary, verify_chain
logfilters.py          configure_logfilters
loginpage.py           login_page
logsafe.py             redact_stream_urls
loyalty.py             award_chat, award_return, configure, enabled, leaderboard, rank_for, status
marketing.py           ai_flavor, class MarketingConfig, class MarketingState, compose, config, configure, default_targets, enabled, has_content, next_due_ts, post_discord, post_telegram, publish, should_post, state, state_save, variants
modheuristics.py       caps_ratio, count_links, count_mentions, escalation_minutes, escalation_step, flood_reason, is_caps_spam, is_exempt, kick_roles, prune_history, prune_infractions, resolve_exempt, stateless_reason, twitch_roles
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
outcomes.py            get_outcome_breakdown
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
preflight.py           configure
procdiag.py            dump_all_threads, prune_stall_dumps, zombie_child_count
proxyutil.py           class ProxyHealth, configure_proxy_select, configure_proxyhealth, configure_router, get_random_proxy, proxy_pool, record_proxy, tunnel_effective, tunnel_state
qrsvg.py               qr_svg
recdb.py               configure, find_recordings_by_fingerprint, get_all_checks, get_all_recordings, get_annotations_for_recording, get_bookmarked_recordings, get_manual_recordings, get_or_compute_inspect_sync, get_recent_recording_attempts, get_recording_by_id, get_recording_note, get_trash_recordings, restore_recording, soft_delete_recording, update_recording_fingerprint
recdiag.py             class RateConfig, class RateSpur, disconnect_analysis, url_refresh_stats
replygate.py           allow, default_config
restream_guard.py      class GuardConfig, class RestreamGuard, class RestreamState, class TargetState, classify
restream_stability.py  budget_after_run, budget_exhausted, class ReconnectPolicy, class StallVerdict, expired_delay, expired_is_spinning, expired_streak, is_codec_failure, looks_like_network_failure, reconnect_delay, stall_verdict
restream_targets.py    active_targets, build_output_args, configure, multistream_targets, single_output_args
restream_testpush.py   build_cmd, class GuardDecision, class ResolvedTarget, class TestPushConfig, classify_result, fingerprint, guard, resolve_target
restream_util.py       betroffene_ziele, fenstergroesse, http_url, looks_like_source_expired, normalize_ingest, slot_belegt, url_host
restreamcfg.py         active_platforms, aktiv, bereite_ziele, chat_src_ok, discord_invite, enabled, ingest, key_gesetzt, kick_channel_url, overlay, stall_timeout, verify, verify_karenz, verify_misses, verify_takt, yt_oauth_configured, ziel
restreamstate.py       guard, haken, laufende, layout_mode, mgr
restrend.py            rising_trend
retention.py           scan
revenue.py             is_revenue_platform, normalisieren, sql_in
schema.py              create_schema
scoring.py             build_report, compute_quality_score
scraper.py             class TikTokScraper, configure_scraper
sendrate.py            allow, default_config, new_state, snapshot
shield.py              —
sqlguard.py            check_readonly, normalize, with_limit
sqlutil.py             —
stats.py               configure_stats, get_activity_pulse, get_lives_heatmap, get_per_user_stats, get_recordings_heatmap, get_stats, get_tiktok_status_distribution, invalidate_stats_cache
storage.py             cleanup, forecast, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
suche.py               universal_search
sysload.py             classify_load, parse_meminfo, parse_ps
sysrun.py              run_priv
textmore.py            configure_banned_cap, split_for_telegram
textutil.py            clean_username, fmt_number, is_valid_tiktok_username, safe, short
tiktokcheck.py         account_exists, configure
tiktokheaders.py       configure
trackingdb.py          add_tracking_tag, bulk_add_trackings, ci_key, claim_transition, configure, get_all_active_trackings, get_all_tags_with_counts, get_priority_poll_interval, get_state, get_tags_for_tracking, get_tracking_priority, get_trackings_for_group, remove_tracking, remove_tracking_tag, resolve_tracked_user, set_tracking_paused, set_tracking_priority
twitchoauth.py         access_token, authorize_url, configure, exchange_code, login_name, search_category, status, timeout_user, update_channel
updater.py             build_plan, check, class Plan, class UpdaterConfig, configure, describe, download_zip, is_protected, job_state, list_backups, local_head, local_state, normalize, remote_head, repo_url, rollback, run_update, settings, sha256_bytes, sha256_file, short_sha, start_update, strip_archive_root, zip_url
usage.py               configure, estimate_tokens, flush, record, snapshot
util.py                datei_in
version.py             changelog, current, latest, summary_line
whispercfg.py          geladen, name, verfuegbar, waehle
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
