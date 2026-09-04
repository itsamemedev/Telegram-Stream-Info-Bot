# NIGHTCRAWLER — Navigationskarte

Erzeugt von `python tools/ncpatch.py map`. Nach jeder Änderung an
Routen, Slash-Commands oder Top-Level-Funktionen neu erzeugen.
Zahlen sind Zeilennummern für `ncpatch show` / `ncpatch sym`.

## Flask-Routen in bot.py (67)

```
 10195  GET              /                                                dashboard
 12573  GET              /api/abo/status                                  api_abo_status
 10268  GET              /api/active-recordings                           api_active_recordings
 12644  GET              /api/activity-pulse                              api_activity_pulse
 12505  DELETE           /api/annotations/<int:aid>                       api_annotation_delete
 11103  GET              /api/automation/status                           api_automation_status
 11125  POST             /api/automation/toggle                           api_automation_toggle
 12537  GET              /api/bandwidth/live                              api_bandwidth_live
 12490  GET              /api/bookmarks                                   api_bookmarks_list
 19354  GET              /api/channel/categories                          api_channel_categories
 19360  POST             /api/channel/set                                 api_channel_set
 19207  GET              /api/channels/status                             api_channels_status
 10249  GET              /api/checks                                      api_checks
 18881  GET/DELETE       /api/clip/<fn>                                   api_clip_file
 18864  GET              /api/clips                                       api_clips
 18910  POST/DELETE      /api/clips/clear                                 api_clips_clear
 12916  GET              /api/community/stats                             api_community_stats
 19791  GET              /api/data/export                                 api_data_export
 18779  GET              /api/debug/threads                               api_debug_threads
 12519  GET              /api/events                                      api_events
 11947  GET              /api/events/stream                               api_events_stream
 12532  GET              /api/forecast/storage                            api_forecast_storage
 11141  GET              /api/freeai/status                               api_freeai_status
 11613  GET              /api/health                                      api_health
 12550  GET              /api/heatmap/lives/<username>                    api_heatmap_lives
 12546  GET              /api/heatmap/recordings                          api_heatmap_recordings
 18811  GET              /api/highlights                                  api_highlights
 18823  POST             /api/highlights/config                           api_highlights_config
 10129  POST             /api/login                                       dashboard_login_submit
 12901  GET              /api/loyalty/leaderboard                         api_loyalty_leaderboard
 12870  GET/POST         /api/notifications/quiet-hours                   api_quiet_hours
 11862  GET              /api/notify/status                               api_notify_status
 11873  POST             /api/notify/test                                 api_notify_test
 10333  GET              /api/outcomes                                    api_outcomes
 12627  GET              /api/proxy/heatmap                               api_proxy_heatmap
 12604  GET              /api/proxy/trend                                 api_proxy_trend
 11479  GET              /api/public/stats                                api_public_stats
 10229  GET              /api/pulse                                       api_pulse
 12124  GET              /api/recording-attempts                          api_recording_attempts
 12475  GET              /api/search                                      api_search
 20314  GET              /api/selftest                                    api_selftest
 18617  GET              /api/shield/stats                                api_shield_stats
 10301  GET              /api/summary/preview                             api_summary_preview
 12189  GET              /api/system                                      api_system
 12949  GET              /api/system/check_timing                         api_check_timing
 13041  GET              /api/system/config_drift                         api_config_drift
 11678  GET              /api/system/config_snapshot                      api_system_config_snapshot
 11720  GET              /api/system/preflight                            api_system_preflight
 11846  GET              /api/system/preflight_history                    api_system_preflight_history
 12012  GET              /api/system/resilience                           api_system_resilience
 12510  GET              /api/tags                                        api_tags_list
 10263  GET              /api/top                                         api_top
 10443  GET              /api/trend-7d                                    api_trend_7d
 18930  GET              /api/tts/<fn>                                    api_tts_file
 19656  GET              /api/upload_window                               api_upload_window
 10347  GET              /api/userstats                                   api_userstats
 11527  GET              /api/version                                     api_version
 12162  GET              /archive/<int:eid>/download                      archive_download
 12219  GET              /download/<int:recording_id>                     download
 12102  GET              /health                                          health
 18748  GET              /healthz                                         healthz
 10120  GET              /login                                           dashboard_login_page
 10150  GET              /logout                                          dashboard_logout
 10157  GET              /manifest.webmanifest                            pwa_manifest
 19629  GET              /overlay                                         overlay_page
 10181  GET              /pwa-icon-<variant>.png                          pwa_icon
 10167  GET              /sw.js                                           pwa_service_worker
```

## Flask-Routen in Blueprints, nc/routes/ (292)

```
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
   184  GET              /api/brain                                       api_brain   [nc/routes/brain.py]
   121  GET              /api/brain/alarms                                api_brain_alarms   [nc/routes/brain.py]
   106  GET              /api/brain/creator                               api_brain_creator   [nc/routes/brain.py]
    83  GET              /api/brain/graph                                 api_brain_graph   [nc/routes/brain.py]
   144  GET              /api/brain/growth                                api_brain_growth   [nc/routes/brain.py]
    70  GET              /api/brain/health                                api_brain_health   [nc/routes/brain.py]
    72  POST             /api/chat/send                                   api_chat_send   [nc/routes/chat.py]
    44  GET              /api/chat/send_status                            api_chat_send_status   [nc/routes/chat.py]
    31  GET              /api/cohost                                      api_cohost   [nc/routes/cohost.py]
    43  POST             /api/cohost/config                               api_cohost_config   [nc/routes/cohost.py]
    42  GET/POST         /api/collections                                 api_collections   [nc/routes/collections.py]
    77  POST/DELETE      /api/collections/<int:cid>                       api_collection_modify   [nc/routes/collections.py]
   112  GET              /api/collections/<int:cid>/trackings             api_collection_trackings   [nc/routes/collections.py]
   274  POST             /api/config/restore                              api_config_restore   [nc/routes/settings.py]
   259  GET              /api/config/snapshot                             api_config_snapshot   [nc/routes/settings.py]
   182  GET              /api/cookies/age                                 api_cookies_age   [nc/routes/settings.py]
    60  GET              /api/cookies/health                              api_cookies_health   [nc/routes/settings.py]
    67  POST             /api/cookies/update                              api_cookies_update   [nc/routes/settings.py]
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
    36  GET              /api/health-score                                api_health_score   [nc/routes/health.py]
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
   210  POST             /api/overlay/config                              api_overlay_config   [nc/routes/overlay.py]
   193  POST             /api/overlay/event                               api_overlay_event   [nc/routes/overlay.py]
    94  GET              /api/overlay/state                               api_overlay_state   [nc/routes/overlay.py]
   168  GET              /api/profile/<username>                          api_profile   [nc/routes/beobachtung.py]
   451  POST             /api/profile/lookup-bulk                         api_profile_lookup_bulk   [nc/routes/beobachtung.py]
   426  GET              /api/profile/snapshots/<username>                api_profile_snapshots   [nc/routes/beobachtung.py]
   823  GET              /api/rec/classify/<int:rec_id>                   api_rec_classify   [nc/routes/recordings.py]
   905  GET              /api/rec/compress-candidates                     api_rec_compress_candidates   [nc/routes/recordings.py]
   933  GET              /api/rec/orphans                                 api_rec_orphans   [nc/routes/recordings.py]
   944  POST             /api/rec/orphans/clean                           api_rec_orphans_clean   [nc/routes/recordings.py]
   810  GET              /api/rec/quality/<int:rec_id>                    api_rec_quality   [nc/routes/recordings.py]
   872  POST             /api/rec/retention/apply                         api_rec_retention_apply   [nc/routes/recordings.py]
   859  POST             /api/rec/retention/preview                       api_rec_retention_preview   [nc/routes/recordings.py]
   840  GET              /api/rec/timeline/<username>                     api_rec_timeline   [nc/routes/recordings.py]
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
   116  GET              /api/system-resources                            api_system_resources   [nc/routes/health.py]
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
 20998  /ai                     
 21457  /ask                    
 21089  /assign_role            
 21135  /ban                    
 21789  /botstats               
 21713  /clearwarns             
 21753  /clip                   
 21738  /clipoftheweek          
 21580  /clips                  
 21050  /create_category        
 21019  /create_channel         
 21078  /create_group           
 21061  /create_role            
 21035  /create_voice           
 21371  /daily                  
 21487  /event                  
 21530  /events                 
 21626  /follow                 
 21610  /help                   
 21124  /kick                   
 21353  /leaderboard            
 21566  /livenow                
 21596  /post_test              
 21427  /profile                
 21159  /purge                  
 21339  /rank                   
 21553  /recstatus              
 21100  /remove_role            
 21012  /restream_status        
 21111  /set_channel_perms      
 21304  /setup_community        
 21322  /setup_targets          
 21652  /stats                  
 20924  /status                 
 21948  /streaminfo             
 21845  /sys_report             
 21821  /sys_unpause            
 21146  /timeout                
 21724  /topstreamers           
 20954  /track                  
 20938  /tracklist              
 21641  /unfollow               
 20987  /untrack                
 21674  /warn                   
 21698  /warnings               
```

## Discord-Events (4)

```
 22434  on_member_join
 22396  on_message
 22035  on_raw_reaction_add
 22469  on_ready
```

## Top-Level-Symbole in bot.py (478 Funktionen, 2 Klassen)

```
  2517-2518   _abo_key
  2538-2556   _abo_probe_dump
 19898-19908  _active_recorder_sync
 15882-15889  _ad_allowlist
 17023-17029  _agent_for
 19910-19928  _ai_calls_total_sync
 17032-17048  _ai_telemetry
 17537-17555  _alert
 22585-22635  _alert_monitor_loop
 22987-23049  _announce_loop
  3459-3462   _anthropic_key
  3469-3471   _anthropic_model
  9873-9876   _arg_int
  2509-2514   _as_dict
 17691-17713  _audio_tap_cmd
 10041-10052  _auth_cookie
 10008-10037  _auth_guard
  1680-1685   _auto_on
 18583-18601  _auto_restream_loop
 24100-24115  _azrael_broadcast_reply
 24000-24022  _azrael_chat_reply
 23983-23997  _azrael_chat_should_reply
 24028-24030  _azrael_gate_cfg
 17053-17067  _azrael_live_state
 19541-19555  _azrael_overlay_state
 17419-17473  _azrael_proactive_loop
 16871-16927  _azrael_reaction_to_chats
 24033-24040  _azrael_reply_all_chats
 23970-23980  _azrael_self_names
 24068-24097  _azrael_send_to
 17073-17094  _azrael_system
 22719-22722  _backup_active
 22800-22813  _backup_loop
 22547-22556  _brain_growth_loop
 10494-10521  _brain_growth_snapshot
  2445-2465   _brain_hint_delay
  6306-6334   _brain_notify
 11926-11943  _browser_push
  6350-6437   _build_daily_summary
  2948-3128   _build_native_cmd
 14070-14257  _build_restream_cmd
  3172-3205   _build_ytdlp_cmd
 19850-19857  _cached_probe
  5128-5155   _can_stop_tracking
  1860-1882   _capture_set_cookies
 12685-12688  _cfg_get
 12691-12693  _cfg_set
 19315-19350  _channel_set_all
 13313-13316  _chat_connected
 13319-13335  _chat_disconnected
  8364-8375   _chat_is_forum
 13355-13357  _chat_sanitize
 13298-13310  _chat_stat
 13338-13341  _chat_stats_snapshot
  3737-3748   _check_ai_alive_sync
  3751-3763   _check_ai_models_sync
 19859-19872  _check_redis_alive_sync
 19874-19894  _check_redis_version_sync
 10776-10819  _classify_pool_anonymity
 10822-10839  _classify_pool_anonymity_bg
   825-829    _claude_chat_sync_metered
  9902-9909   _client_ip
 23081-23108  _clip_prune
 23111-23121  _clip_recfile_for
 23634-23640  _clip_should_velocity
 23162-23244  _clip_to_discord
  3635-3644   _close_ai_session
 24146-24161  _cohost_broadcast
 24131-24132  _cohost_cfg
 24187-24199  _cohost_fire_highlight
 24135-24143  _cohost_gate
 24164-24184  _cohost_highlight
 23293-23327  _community_events_loop
 10394-10396  _conv_messages
  6706-6749   _cookie_alarm_loop
  1932-1936   _cookie_autorefresh_info
  1837-1841   _cookie_header
 11976-12008  _cpu_load_snapshot
  3957-3969   _create_index_safe
 20092-20198  _crowdsec_status
 20038-20089  _crowdsec_via_lapi
 19942-19960  _cscli_bin
 19969-19982  _cscli_path
  6596-6621   _daily_summary_loop
 20000-20017  _darf_journal_lesen
 22559-22582  _db_maintenance_loop
  6565-6593   _db_vacuum_loop
 15905-15929  _detect_foreign_ad
  1418-1429   _diag_path_owner
 17325-17369  _director_finalize
 18137-18144  _director_for
 17274-17322  _director_mark
 23528-23563  _disc_automod_check
 23504-23507  _disc_state_get
 23510-23517  _disc_state_set
 20574-20587  _discord_guild_filesize_bytes
 20781-20785  _discord_invite
 23465-23501  _discord_live_thread
 17476-17488  _discord_notify
 20680-20705  _discord_ops_alert
 23363-23461  _discord_post_user
 20841-22544  _discord_run_once
 20720-20778  _discord_start
 23052-23058  _discord_stop
 20595-20597  _discord_upload_limit_label
 20590-20592  _discord_upload_limit_mb
  6624-6701   _disk_alarm_loop
 25579-25628  _disk_autoclean
 25631-25644  _disk_guard_loop
 25571-25576  _disk_pct
 13663-13665  _drawtext_chain
 12318-12320  _dump_all_threads
 10702-10765  _enrich_proxies_with_geo
  2077-2121   _ensure_cookie_file_netscape
 20788-20838  _ensure_discord_invite
 23258-23290  _ensure_error_channel
  8423-8426   _ensure_notify_topic
 10946-10983  _ensure_proxy_ready
  8377-8404   _ensure_topic
   682-684    _env_int
   687-689    _env_int_range
 23330-23360  _error_channel_loop
 17521-17534  _event_webhook
 13128-13141  _evolution_loop
  5748-5782   _extract_file_payload
  2193-2195   _extract_urls_from_streamurl_node
 19985-19992  _f2b_sudo_hint
 17557-17559  _faster_whisper_available
 10603-10621  _fetch_proxy_list
 17971-17999  _fetch_tiktok_room_id
   758-761    _ff_cmd
 13829-13834  _find_chromium
  3165-3169   _find_external_recorder
  2198-2200   _find_stream_urls
 12736-12761  _fire_webhooks
  7486-7495   _fork_safe
   840-849    _freeai_chat_sync_metered
 20031-20035  _geo_lookup_ips
  3623-3632   _get_ai_session
  7319-7359   _get_live_info
  2735-2742   _get_resolve_semaphore
  7719-8085   _handle_single_tracking
 25397-25399  _hb
 25402-25419  _hb_while
 13364-13366  _highlight_cfg
 13369-13398  _highlight_observe
 13837-13855  _htmlov_screenshot_cmd
 17715-17725  _httpx_proxy
 12769-12781  _in_quiet_hours
 26470-26501  _install_fast_eventloop
  9768-9822   _install_fast_json
 12323-12339  _install_faulthandler
 18656-18665  _intel_ensure_schema
 18703-18738  _intel_index_loop
 18677-18687  _intel_index_one
 18668-18674  _intel_semantic
  5117-5126   _is_authorized
  7620-7626   _is_dead
  2183-2185   _is_hevc
 20020-20022  _is_private_ip
  1582-1589   _is_process_running
  6336-6347   _is_quiet_hours
  1219-1228   _is_upload_window
  9857-9870   _json_error_handler
  6559-6560   _kick_broadcaster_id
  6471-6513   _kick_follower_count
  6455-6458   _kick_slug
 11554-11585  _kick_user_token
  4006-4009   _kind_from_filename
 12798-12803  _latest_popularity
 18352-18385  _live_react_loop
 18148-18341  _live_react_worker
 16930-16941  _live_transcript_push
 18343-18350  _live_users
 17372-17416  _living_title_loop
  1758-1831   _load_cookies_dict
 22725-22797  _local_backup_scan
  9839-9853   _log_5xx
 14265-14277  _looks_like_codec_err
 14260-14262  _looks_like_source_expired
  7536-7566   _loop_fehler
 12343-12352  _loop_heartbeat
 25367-25394  _loop_lag_monitor
 12355-12423  _loop_watchdog_thread
 16810-16824  _loyalty_add
 16801-16807  _loyalty_get
 16827-16835  _loyalty_top
 12935-12937  _manual_donations_total
  7628-7629   _mark_dead
 11232-11248  _marketing_loop
 24047-24065  _maybe_handle_command
 25730-25754  _maybe_hype_clip
  3924-3947   _migrate_columns
 24326-24337  _mod_is_exempt
 24340-24345  _mod_warn_first
 24348-24351  _mod_warn_text
 13168-13176  _modlog
   970-972    _multistream_targets
  7498-7499   _nc_create_subprocess_exec
  7502-7503   _nc_create_subprocess_shell
 11484-11501  _news_loop
 13195-13197  _normalize_ingest
  2376-2393   _note_check_duration
  8417-8420   _notify_topic_name
 16956-16964  _oracle_memories
 17229-17263  _oracle_memorize
 16967-16980  _oracle_persona
 16949-16953  _oracle_recent_text
 13489-13497  _ov_atomic_write
 13477-13483  _ov_bar
 15808-15820  _ov_clip_text
 13486-13487  _ov_oneline
 19593-19622  _overlay_push
 13783-13826  _overlay_render_size
 13261-13265  _overlay_session_reset
 19557-19560  _overlay_src_ok
 15892-15902  _own_invites
 13778-13780  _parse_size
 20206-20286  _parse_ssh_attacks
  6921-6954   _pause_resume_cmd
  1886-1930   _persist_refreshed_cookies
  1724-1756   _pick_checked_pull_proxy
  9938-9951   _pin_auth_value
  9997-9998   _pin_clear_fail
  9977-9980   _pin_locked
  9983-9994   _pin_note_fail
  9954-9974   _pin_ok
 19451-19476  _piper_pick_model
 19488-19535  _piper_say
 12698-12733  _post_json_threaded
 13757-13775  _probe_video_size
  1610-1627   _proc_is_recorder
 10915-10943  _proxy_pool_refresh_loop
  1690-1721   _proxy_report_recording
 12308-12310  _prune_stall_dumps
 11302-11423  _public_stats
 17492-17518  _push_notify
 10099-10101  _pwa_dir
 10672-10687  _quick_validate_proxy
 12764-12766  _quiet_hours_config
 10064-10097  _rate_guard
 16775-16781  _react_warn
  7406-7445   _reap_proc
  2416-2438   _record_check_outcome
   753-755    _redact_stream_urls
 10842-10912  _refresh_proxy_pool
  2209-2299   _resolve_via_html
  2558-2712   _resolve_via_webcast_api_v2
  2775-2837   _resolve_via_ytdlp
 23674-23803  _resolve_youtube_ingest
 13244-13255  _restream_active_sources
 18002-18101  _restream_chat_guardian
 13401-13473  _restream_chat_push
 13858-13945  _restream_html_overlay_start
 13948-13961  _restream_html_overlay_stop
 13206-13229  _restream_overlay_files
 18389-18421  _restream_platform_state
 18545-18580  _restream_resume_after_restart
 14009-14067  _restream_tts_enqueue_wav
 13719-13751  _restream_tts_feeder
 13716-13717  _restream_tts_fifo_path
 13964-13991  _restream_tts_start
 13993-14007  _restream_tts_stop
 18427-18542  _restream_verify_loop
 22690-22702  _retention_loop
 22684-22687  _retention_scan
  2520-2522   _room_is_abo
  5786-5903   _run_ai_call
 12446-12459  _run_async_from_flask
 20025-20028  _run_priv
 26458-26466  _run_selfcheck_and_exit
 22705-22716  _s3_client
  7655-7706   _safe_send
  4628-4644   _sample_net_throughput
  2468-2495   _schedule_next_check
 22638-22681  _scheduler_loop
  3950-3954   _schema_pk
 12463-12468  _scraper_session
 24354-24393  _screen_full
 11629-11666  _sec_headers
  2188-2190   _select_stream_from_data_section
 26271-26455  _selfcheck
  8429-8463   _send_live_notice
  1242-1246   _should_defer_upload
 23124-23159  _shrink_for_discord
 10104-10116  _sicheres_ziel
 25651-25668  _sign_health_check
 25671-25690  _sign_health_loop
  7515-7526   _spawn
 26730-26760  _spawn_from_flask
 20307-20310  _st_befund
 17727-17968  _start_chat_listener
 12426-12443  _start_loop_watchdog
 11447-11475  _stats_loop
 11426-11429  _stats_output_path
 11432-11444  _stats_write
  8157-8173   _storage_cleanup_loop
 25710-25717  _story_for
  3227-3233   _stream_url_expiry
  3242-3248   _stream_url_is_fresh
  3235-3240   _stream_url_ttl
 15855-15862  _streamer_persona_get
 13668-13672  _studio_chain
 22822-22944  _system_backup
 22953-22983  _system_backup_loop
 10624-10663  _test_proxy
 11180-11196  _testpush_resolve_live
  7631-7652   _tg_sprache_setzen
  8336-8346   _tg_topics_load_into_mem
  8333-8334   _tg_topics_path
  8348-8355   _tg_topics_save
  9912-9920   _token_ok
  8358-8362   _topic_forget
 12784-12795  _tracking_max_duration
  4215-4229   _tracking_remove_cleanup
  4246-4258   _tracking_resume_cleanup
  1476-1499   _try_attach_file_handler
 19478-19486  _tts_cleanup
 11156-11160  _tunnel_effective
 18974-19027  _twitch_channel_status
 24396-24541  _twitch_chat_loop
 24210-24313  _twitch_eventsub_loop
  1265-1278   _upload_queue_add
  1289-1291   _upload_queue_count
  1248-1257   _upload_queue_load
  1238-1240   _upload_queue_path
  1280-1287   _upload_queue_remove
  1259-1263   _upload_queue_save
  1293-1334   _upload_window_loop
  7379-7386   _uptime_s
 13183-13192  _url_host
   733-750    _url_ohne_zugang
   818-822    _usage_record_claude
  7569-7613   _verbindung_verloren
  6516-6547   _viewer_sample_loop
 10001-10004  _wants_html
  7389-7403   _warn_empty_env
 25440-25561  _watchdog_loop
 23949-23957  _wchat_thank_ok
 17561-17591  _whisper_get_model
  7476-7483   _whisper_native_section
 16762-16768  _whisper_pool
 17660-17689  _whisper_segments
 17593-17657  _whisper_transcribe
 13499-13661  _write_restream_overlay
 24565-24645  _youtube_api_chat_loop
 19030-19133  _youtube_api_status
 19136-19203  _youtube_channel_status
 24648-24809  _youtube_chat_loop
 23809-23822  _youtube_restream_autoconfig
 23825-23849  _youtube_restream_autoconfig_inner
 23916-23944  _youtube_send
 19271-19312  _youtube_set_channel
 23852-23886  _yt_access_token
 23889-23904  _yt_live_chat_id
 23912-23913  _yt_sendrate_cfg
 24544-24559  _yt_timeout
  2759-2760   _ytdlp_detect_available
  2762-2773   _ytdlp_note_result
 12313-12315  _zombie_child_count
  7255-7279   about
  4125-4129   add_ai_log_entry
  4042-4045   add_archive_entry
  4705-4707   add_archive_rule
  4417-4451   add_recording
  4190-4207   add_tracking
  5906-5939   ai
  3777-3828   ai_chat
  3862-3872   ai_history_append
  3874-3879   ai_history_clear
  3851-3860   ai_history_load
  3836-3849   ai_rate_limit_check
  5968-5976   aireset
 17097-17116  azrael_chat
 24814-24936  brain_cmd
  3251-3435   build_recording_cmd
  4210-4213   bulk_add_trackings
  6752-6811   bulkadd
  8176-8316   check_all_trackings
  4262-4274   claim_live_transition
 15932-16694  class KickModerator
 14280-15695  class RestreamManager
 11029-11071  classify_proxy_anonymity
  6014-6212   cleanup
  5012-5018   cleanup_old_recordings
  4408-4415   clear_recording
 23566-23631  clip_moment
  4572-4621   compute_storage_forecast
  6874-6918   cookies_cmd
  4181-4187   count_trackings_for_chat
  4112-4123   decide_preferred_recorder
  4052-4055   delete_archive_entry
  4709-4711   delete_archive_rule
  5443-5590   diag
 25048-25109  einnahmen_cmd
  4566-4569   find_recordings_by_fingerprint
  4073-4089   finish_recording_attempt
  4234-4236   get_all_active_trackings
  4140-4143   get_all_checks
  4453-4456   get_all_recordings
  4515-4517   get_all_tags_with_counts
  4543-4546   get_annotations_for_recording
  4047-4050   get_archive_entry
  4536-4539   get_bookmarked_recordings
  1953-2070   get_cookie_health
  4503-4509   get_event_log
  4096-4110   get_last_recording_attempt
  2840-2945   get_live_status
  4894-4897   get_manual_recordings
  4551-4554   get_or_compute_inspect_sync
  5053-5097   get_outcome_breakdown
  4522-4525   get_priority_poll_interval
  4091-4094   get_recent_recording_attempts
  4458-4461   get_recording_by_id
  4529-4532   get_recording_note
  3569-3592   get_redis
  4170-4173   get_stats
  5006-5010   get_storage_stats
  4729-4731   get_tiktok_status_distribution
  4276-4285   get_tracking_state
  4231-4232   get_trackings_for_group
  4910-4913   get_trash_recordings
  9084-9747   handle_recording_finished
  3972-3997   init_db
  4701-4703   list_archive_rules
  5247-5285   live
  7709-7717   live_check_worker
  3647-3681   llm_chat
  3704-3732   llm_chat_sync
  3689-3701   llm_list_models
  4469-4495   log_event
  1544-1577   log_recording_failure
  7068-7117   logs_cmd
 25758-26261  main
  5942-5965   on_ai_media
  7194-7220   on_ai_reply
  7223-7252   on_azrael_mention
  7284-7314   on_callback
 17122-17226  oracle_handle
  6957-6960   pause_tracking
  5107-5112   profile_keyboard
  7019-7065   quota
  8087-8154   reaper_loop
  4725-4727   record_tiktok_status
  5981-6011   recstatus
  3594-3602   redis_get_json
  3605-3611   redis_set_json
 25112-25122  report_cmd
 11074-11076  report_proxy_result
  2302-2329   resolve_tiktok_live_stream
  4905-4908   restore_recording
  6963-6966   resume_tracking
  4714-4719   run_archive_rules
 25125-25347  run_bot
 12233-12280  run_flask
  4647-4692   sample_bandwidth_for_active
  4132-4138   save_tiktok_check
  4400-4406   set_recording_file
  4239-4243   set_tracking_paused
  4900-4903   soft_delete_recording
  8469-9082   split_and_send_video
  5160-5202   start
  4057-4071   start_recording_attempt
  6215-6253   stats
  4875-4892   stop_manual_recording
  6969-7016   stoprec
  6440-6448   summary_cmd
  7120-7191   sysres
  5592-5736   teststream
  5204-5245   tiktok
  6814-6871   topusers
  5322-5379   track
  5287-5319   track_exact
  5393-5441   tracklist
  4741-4873   trigger_manual_recording
  4361-4398   try_acquire_recording_lock
  4916-4975   universal_search
  5381-5391   untrack
 24939-25045  update_cmd
  4561-4564   update_recording_fingerprint
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
binresolve.py          resolve
brainstate.py          history_for, record, stall, stream_recent
cfgnorm.py             normalize_audio, normalize_cohost, normalize_gate, normalize_highlights, normalize_quiet_hours, normalize_sendrate
cfgstore.py            get, set_, upsert
channels.py            configure_chat, restream_active, yt_sendrate_cfg
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
modstats.py            ist_moderation, plattform, quellen, verdichte, zaehlt
netstat.py             sum_bytes, throughput_kbps
news.py                absaetze, azrael_creator_take, build_items, class NewsConfig, class NewsState, collect_facts, config, configure, creator_activity, creator_dossier_generate, creator_facts_line, enabled, generate, item_id, merge, output_path, phrase, phrase_impl, read_items, render_json, should_generate, state, state_save, write_items
notes.py               add_annotation, delete_annotation, set_recording_note, set_tracking_notes, toggle_bookmark
oauthpage.py           kick, twitch
oauthredirect.py       configure, public_base_url, redirect_env, redirect_public, redirect_source, redirect_uri
persona.py             —
piper_voices.py        available, bin_pfad, configure, data_dir, list_voices, resolve, resolve_model_path, roots, voice_dirs, voice_roots
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
storage.py             cleanup, stats
story.py               class StoryMemory, configure
streamsel.py           extract_urls_from_streamurl_node, find_stream_urls, is_hevc, select_stream_from_data_section
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
